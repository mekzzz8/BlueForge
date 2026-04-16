from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blueforge.db'
app.secret_key = 'blueforge-dev-key-2025'

db = SQLAlchemy(app)

SCENARIOS = [
    {
        "id": "sc-001",
        "nombre": "Operación NightCrypt",
        "empresa": "FinCorp Solutions S.A.",
        "tipo": "Ransomware · Incident Response",
        "dificultad": "medium",
        "siem": "Elastic Stack",
        "puntos_max": 1000,
        "bloqueado": False,
        "desc": "FinCorp Solutions sufre cifrado masivo a las 3AM. Analiza los logs de Windows para reconstruir la cadena de ataque completa.",
        "briefing": "El 14 de noviembre a las 03:14 UTC el equipo de seguridad de FinCorp Solutions detectó actividad anómala en sus servidores. En menos de 20 minutos, el 80% de los ficheros corporativos aparecieron cifrados con extensión .ncrypt. Tu misión es reconstruir toda la cadena de ataque: cómo entraron, qué ejecutaron, cómo se mantuvieron y cuándo comenzó el cifrado.",
        "herramientas": ["Kibana", "Volatility", "Wireshark"],
        "tecnicas_mitre": ["T1566.001", "T1059.001", "T1547.001", "T1486"],
        "objetivos": [
    {
        "id": "OBJ-001",
        "pregunta": "¿Cuál es el nombre del proceso malicioso que inició el ataque?",
        "categoria": "Threat Hunting",
        "flag": "svchost_fake.exe",
        "puntos": 150,
        "hints": [
            {"nivel": 1, "coste": 0,   "archivo": "hint-obj001-1.md"},
            {"nivel": 2, "coste": 50,  "archivo": "hint-obj001-2.md"},
            {"nivel": 3, "coste": 100, "archivo": "hint-obj001-3.md"}
        ]
    },
    {
        "id": "OBJ-002",
        "pregunta": "¿Qué dirección IP externa contactó el malware durante la fase C2?",
        "categoria": "Network Forensics",
        "flag": "185.220.101.47",
        "puntos": 200,
        "hints": [
            {"nivel": 1, "coste": 0,   "archivo": "hint-obj002-1.md"},
            {"nivel": 2, "coste": 50,  "archivo": "hint-obj002-2.md"},
            {"nivel": 3, "coste": 100, "archivo": "hint-obj002-3.md"}
        ]
    },
    {
        "id": "OBJ-003",
        "pregunta": "¿Qué clave de registro usó el malware para establecer persistencia?",
        "categoria": "Incident Response",
        "flag": "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
        "puntos": 250,
        "hints": [
            {"nivel": 1, "coste": 0,   "archivo": "hint-obj003-1.md"},
            {"nivel": 2, "coste": 50,  "archivo": "hint-obj003-2.md"},
            {"nivel": 3, "coste": 100, "archivo": "hint-obj003-3.md"}
        ]
    }
]

    },

    {
        "id": "sc-002",
        "nombre": "Operación SilentMove",
        "empresa": "GovTech Ministerio",
        "tipo": "APT · Lateral Movement",
        "dificultad": "hard",
        "siem": "Splunk",
        "puntos_max": 2000,
        "bloqueado": True,
        "desc": "Próximamente disponible."
    }
]

@app.route('/')
def dashboard():
    return render_template('dashboard.html', scenarios=SCENARIOS)

@app.route('/scenario/<scenario_id>')
def scenario(scenario_id):
    sc = next((s for s in SCENARIOS if s['id'] == scenario_id), None)
    if sc is None:
        return "Escenario no encontrado", 404
    return render_template('scenario.html', scenario=sc)

@app.route('/submit/<scenario_id>/<obj_id>', methods=['POST'])
def submit(scenario_id, obj_id):
    from flask import request, session

    sc = next((s for s in SCENARIOS if s['id'] == scenario_id), None)
    if sc is None:
        return jsonify({"error": "Escenario no encontrado"}), 404

    obj = next((o for o in sc['objetivos'] if o['id'] == obj_id), None)
    if obj is None:
        return jsonify({"error": "Objetivo no encontrado"}), 404

    # Inicializar progreso en sesión si no existe
    if 'progreso' not in session:
        session['progreso'] = {}

    # Si ya fue resuelto no hacer nada
    if obj_id in session['progreso']:
        return jsonify({
            "correcta": True,
            "mensaje": "Ya resolviste este objetivo.",
            "puntos": 0
        })

    respuesta = request.form.get('respuesta', '').strip()
    correcta = respuesta == obj['flag']

    if correcta:
        session['progreso'][obj_id] = {
            "scenario_id": scenario_id,
            "puntos": obj['puntos']
        }
        session.modified = True

    return jsonify({
        "correcta": correcta,
        "mensaje": "¡Correcto! +{} puntos".format(obj['puntos']) if correcta else "Incorrecto, sigue investigando.",
        "puntos": obj['puntos'] if correcta else 0
    })

@app.route('/api/progreso')
def api_progreso():
    from flask import session
    progreso = session.get('progreso', {})
    total_puntos = sum(v['puntos'] for v in progreso.values())
    return jsonify({
        "objetivos_resueltos": list(progreso.keys()),
        "total_puntos": total_puntos
    })

@app.route('/health')
def health():
    return jsonify({"status": "online", "platform": "BlueForge"})

@app.route('/progress')
def progress():
    return render_template('progress.html')

@app.route('/hint/<scenario_id>/<obj_id>/<int:nivel>', methods=['POST'])
def get_hint(scenario_id, obj_id, nivel):
    from flask import session
    import os

    sc = next((s for s in SCENARIOS if s['id'] == scenario_id), None)
    if sc is None:
        return jsonify({"error": "Escenario no encontrado"}), 404

    obj = next((o for o in sc['objetivos'] if o['id'] == obj_id), None)
    if obj is None:
        return jsonify({"error": "Objetivo no encontrado"}), 404

    hint = next((h for h in obj['hints'] if h['nivel'] == nivel), None)
    if hint is None:
        return jsonify({"error": "Hint no encontrado"}), 404

    # Inicializar hints en sesión
    if 'hints_usados' not in session:
        session['hints_usados'] = {}

    hint_key = f"{obj_id}-nivel{nivel}"

    # Si ya fue usado devolver el contenido sin cobrar
    if hint_key in session['hints_usados']:
        return jsonify({
            "contenido": session['hints_usados'][hint_key],
            "coste": 0,
            "ya_usado": True
        })

    # Verificar puntos suficientes para hints de pago
    if hint['coste'] > 0:
        total_puntos = sum(
            v['puntos'] for v in session.get('progreso', {}).values()
        )
        hints_gastados = sum(
            h['coste'] for h in session['hints_usados'].values()
            if isinstance(h, dict) and 'coste' in h
        )
        puntos_disponibles = total_puntos - hints_gastados
        if puntos_disponibles < hint['coste']:
            return jsonify({
                "error": f"Puntos insuficientes. Necesitas {hint['coste']} pts."
            }), 403

    # Leer el archivo de hint
    hint_path = os.path.join(
        '..', 'scenarios', scenario_id + '-ransomware',
        'hints', hint['archivo']
    )
    
    # Ruta absoluta desde la raíz del proyecto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hint_path = os.path.join(
        base_dir, 'scenarios', 'sc-001-ransomware',
        'hints', hint['archivo']
    )

    try:
        with open(hint_path, 'r', encoding='utf-8') as f:
            contenido = f.read().strip()
    except FileNotFoundError:
        return jsonify({"error": "Archivo de hint no encontrado"}), 404

    # Guardar en sesión
    session['hints_usados'][hint_key] = contenido
    session.modified = True

    return jsonify({
        "contenido": contenido,
        "coste": hint['coste'],
        "nivel": nivel,
        "ya_usado": False
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)