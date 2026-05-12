import os
import json
from flask import Flask, render_template, jsonify, request, session

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'blueforge-v2-dev-key-2025'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES_DIR = os.path.join(BASE_DIR, 'cases')

PHASE_LABELS = {
    'email':      {'icon': '📧', 'label': 'Email'},
    'win_logs':   {'icon': '📋', 'label': 'Windows Logs'},
    'net_logs':   {'icon': '🌐', 'label': 'Red'},
    'server_logs':{'icon': '🐧', 'label': 'Servidor'},
    'terminal':   {'icon': '💻', 'label': 'Terminal'},
    'verdict':    {'icon': '⚖️',  'label': 'Veredicto'},
}

def load_all_cases():
    cases = []
    if not os.path.exists(CASES_DIR):
        return cases
    for case_dir in sorted(os.listdir(CASES_DIR)):
        meta_path = os.path.join(CASES_DIR, case_dir, 'metadata.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r', encoding='utf-8') as f:
                cases.append(json.load(f))
    return cases

def find_case_dir(case_id):
    """Find the directory for a case_id, supporting both 'caso-001' and 'caso-001-darkmail' formats."""
    if not os.path.exists(CASES_DIR):
        return None
    # Exact match first
    exact = os.path.join(CASES_DIR, case_id)
    if os.path.isdir(exact):
        return exact
    # Prefix match (caso-001 → caso-001-darkmail)
    for d in os.listdir(CASES_DIR):
        if d.startswith(case_id):
            return os.path.join(CASES_DIR, d)
    return None

def load_case(case_id):
    case_dir = find_case_dir(case_id)
    if not case_dir:
        return None
    meta_path = os.path.join(case_dir, 'metadata.json')
    if not os.path.exists(meta_path):
        return None
    with open(meta_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_phase(case_id, phase):
    case_dir = find_case_dir(case_id)
    if not case_dir:
        return None
    path = os.path.join(case_dir, f'{phase}.json')
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_progreso():
    return session.get('progreso_v2', {})

def get_total_puntos(progreso):
    return sum(
        v.get('puntos', 0) for v in progreso.values()
        if isinstance(v, dict)
    )

def case_status(case_id, fases, progreso):
    completed = [f for f in fases if f'{case_id}:{f}' in progreso]
    if not completed:
        return 'open'
    if len(completed) == len(fases):
        return 'done'
    return 'active'


@app.route('/')
def dashboard():
    cases = load_all_cases()
    progreso = get_progreso()
    total_puntos = get_total_puntos(progreso)
    cases_done = sum(
        1 for c in cases
        if case_status(c['id'], c.get('fases', []), progreso) == 'done'
    )
    return render_template(
        'dashboard.html',
        cases=cases,
        progreso=progreso,
        total_puntos=total_puntos,
        cases_done=cases_done,
        phase_labels=PHASE_LABELS,
        case_status=case_status,
    )


@app.route('/case/<case_id>')
def case(case_id):
    caso = load_case(case_id)
    if not caso:
        return "Caso no encontrado", 404
    phases = {}
    for phase in caso.get('fases', []):
        data = load_phase(case_id, phase)
        if data:
            phases[phase] = data
    progreso = get_progreso()
    return render_template(
        'case.html',
        caso=caso,
        phases=phases,
        progreso=progreso,
        phase_labels=PHASE_LABELS,
    )


@app.route('/api/case/<case_id>/phase/<phase>/complete', methods=['POST'])
def complete_phase(case_id, phase):
    caso = load_case(case_id)
    if not caso:
        return jsonify({'error': 'Caso no encontrado'}), 404

    if 'progreso_v2' not in session:
        session['progreso_v2'] = {}

    key = f'{case_id}:{phase}'
    if key in session['progreso_v2']:
        return jsonify({'ok': True, 'ya_completada': True, 'puntos': 0})

    puntos = caso.get('fase_puntos', {}).get(phase, 100)
    session['progreso_v2'][key] = {'case_id': case_id, 'phase': phase, 'puntos': puntos}
    session.modified = True

    return jsonify({'ok': True, 'ya_completada': False, 'puntos': puntos})


@app.route('/api/case/<case_id>/verdict', methods=['POST'])
def submit_verdict(case_id):
    data = request.get_json()
    verdict_data = load_phase(case_id, 'verdict')
    if not verdict_data:
        return jsonify({'error': 'Veredicto no encontrado'}), 404

    respuestas = data.get('respuestas', {})
    total_puntos = 0
    resultados = {}

    for q in verdict_data.get('preguntas', []):
        qid = q['id']
        respuesta = respuestas.get(qid, '')
        correcta = respuesta == q['respuesta_correcta']
        puntos = q['puntos'] if correcta else q.get('penalizacion', 0)
        total_puntos += puntos
        resultados[qid] = {
            'correcta': correcta,
            'puntos': puntos,
            'respuesta_correcta': q['respuesta_correcta'],
            'feedback': q['feedback_correcto'] if correcta else q['feedback_incorrecto'],
        }

    if 'progreso_v2' not in session:
        session['progreso_v2'] = {}

    key = f'{case_id}:verdict'
    session['progreso_v2'][key] = {
        'case_id': case_id,
        'phase': 'verdict',
        'puntos': max(0, total_puntos),
        'resultados': resultados,
    }
    session.modified = True

    return jsonify({'ok': True, 'total_puntos': total_puntos, 'resultados': resultados})


@app.route('/api/hint/<case_id>/<qid>/<int:nivel>', methods=['POST'])
def get_hint(case_id, qid, nivel):
    verdict_data = load_phase(case_id, 'verdict')
    if not verdict_data:
        return jsonify({'error': 'No encontrado'}), 404

    pregunta = next((q for q in verdict_data.get('preguntas', []) if q['id'] == qid), None)
    if not pregunta:
        return jsonify({'error': 'Pregunta no encontrada'}), 404

    hint = next((h for h in pregunta.get('hints', []) if h['nivel'] == nivel), None)
    if not hint:
        return jsonify({'error': 'Hint no encontrado'}), 404

    hint_key = f'hint:{case_id}:{qid}:{nivel}'
    if 'hints_usados' not in session:
        session['hints_usados'] = {}

    if hint_key in session['hints_usados']:
        return jsonify({'contenido': hint['contenido'], 'coste': 0, 'ya_usado': True})

    coste = hint.get('coste', 0)
    if coste > 0:
        progreso = get_progreso()
        total = get_total_puntos(progreso)
        ya_gastado = sum(
            h.get('coste', 0) for h in session['hints_usados'].values()
            if isinstance(h, dict)
        )
        if total - ya_gastado < coste:
            return jsonify({'error': f'Necesitas {coste} pts disponibles'}), 403

    session['hints_usados'][hint_key] = {'coste': coste}
    session.modified = True

    return jsonify({'contenido': hint['contenido'], 'coste': coste, 'ya_usado': False})


@app.route('/api/progreso')
def api_progreso():
    progreso = get_progreso()
    return jsonify({'progreso': progreso, 'total_puntos': get_total_puntos(progreso)})

@app.route('/api/reset', methods=['POST'])
def api_reset():
    session.pop('progreso_v2', None)
    return jsonify({'ok': True})


@app.route('/progress')
def progress():
    cases = load_all_cases()
    progreso = get_progreso()
    total_puntos = get_total_puntos(progreso)
    return render_template(
        'progress.html',
        cases=cases,
        progreso=progreso,
        total_puntos=total_puntos,
        phase_labels=PHASE_LABELS,
        case_status=case_status,
    )


@app.route('/learn')
def learn():
    return render_template('learn.html')


@app.route('/siem-lab')
def siem_lab():
    return render_template('siem_lab.html')


@app.route('/health')
def health():
    return jsonify({'status': 'online', 'platform': 'BlueForge', 'version': '2.0'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
