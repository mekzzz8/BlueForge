from flask import Flask, render_template, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
import os

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
        ],
        "tickets": [
            {
                "id": "TKT-001",
                "titulo": "Alerta: Proceso sospechoso detectado en WKSTN-042",
                "severidad": "alta",
                "descripcion": "El EDR ha detectado la creación de svchost_fake.exe desde C:\\Users\\Public\\. El proceso estableció conexión saliente a IP externa. Host afectado: WKSTN-042, Usuario: j.martinez.",
                "acciones": [
                    {
                        "id": "A1",
                        "texto": "Aislar el host WKSTN-042 de la red inmediatamente",
                        "puntos": 100,
                        "impacto": 0,
                        "correcto": True,
                        "feedback": "Correcto. Aislar el host evita propagación lateral y corta la comunicación C2 sin afectar al negocio."
                    },
                    {
                        "id": "A2",
                        "texto": "Apagar el servidor de base de datos para contener la amenaza",
                        "puntos": -200,
                        "impacto": 200,
                        "correcto": False,
                        "feedback": "Incorrecto. Apagar el servidor de BD en horario laboral causa pérdida de datos y paraliza operaciones."
                    },
                    {
                        "id": "A3",
                        "texto": "Notificar al CISO y abrir proceso formal de Incident Response",
                        "puntos": 150,
                        "impacto": 0,
                        "correcto": True,
                        "feedback": "Correcto. Escalar al CISO es obligatorio ante un incidente confirmado. Activa el proceso IR formal."
                    },
                    {
                        "id": "A4",
                        "texto": "Ignorar la alerta — puede ser un falso positivo",
                        "puntos": -300,
                        "impacto": 300,
                        "correcto": False,
                        "feedback": "Incorrecto. Ignorar una alerta de proceso sospechoso con conexión C2 activa es una negligencia grave."
                    }
                ]
            },
            {
                "id": "TKT-002",
                "titulo": "Alerta: Modificación de clave de registro Run detectada",
                "severidad": "media",
                "descripcion": "Sysmon reporta modificación de HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run en WKSTN-042. Valor añadido: svchost_update apuntando a C:\\Users\\Public\\.",
                "acciones": [
                    {
                        "id": "B1",
                        "texto": "Documentar el IOC y añadirlo a las reglas de detección del SIEM",
                        "puntos": 100,
                        "impacto": 0,
                        "correcto": True,
                        "feedback": "Correcto. Documentar IOCs mejora la detección futura y enriquece la inteligencia de amenazas."
                    },
                    {
                        "id": "B2",
                        "texto": "Eliminar la clave de registro sin preservar evidencias forenses",
                        "puntos": -150,
                        "impacto": 150,
                        "correcto": False,
                        "feedback": "Incorrecto. Eliminar evidencias antes de preservarlas destruye la cadena de custodia forense."
                    },
                    {
                        "id": "B3",
                        "texto": "Realizar volcado de memoria del host antes de cualquier acción",
                        "puntos": 200,
                        "impacto": 0,
                        "correcto": True,
                        "feedback": "Correcto. El volcado de memoria captura el estado del malware en ejecución — información crítica para el análisis forense."
                    }
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
    sc = next((s for s in SCENARIOS if s['id'] == scenario_id), None)
    if sc is None:
        return jsonify({"error": "Escenario no encontrado"}), 404

    obj = next((o for o in sc['objetivos'] if o['id'] == obj_id), None)
    if obj is None:
        return jsonify({"error": "Objetivo no encontrado"}), 404

    if 'progreso' not in session:
        session['progreso'] = {}

    if obj_id in session['progreso']:
        return jsonify({"correcta": True, "mensaje": "Ya resolviste este objetivo.", "puntos": 0})

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
    progreso = session.get('progreso', {})
    tickets_resueltos = session.get('tickets_resueltos', {})
    total_puntos = sum(v['puntos'] for v in progreso.values())
    total_puntos += sum(v['puntos'] for v in tickets_resueltos.values())
    return jsonify({
        "objetivos_resueltos": list(progreso.keys()),
        "tickets_resueltos": tickets_resueltos,
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
    sc = next((s for s in SCENARIOS if s['id'] == scenario_id), None)
    if sc is None:
        return jsonify({"error": "Escenario no encontrado"}), 404

    obj = next((o for o in sc['objetivos'] if o['id'] == obj_id), None)
    if obj is None:
        return jsonify({"error": "Objetivo no encontrado"}), 404

    hint = next((h for h in obj['hints'] if h['nivel'] == nivel), None)
    if hint is None:
        return jsonify({"error": "Hint no encontrado"}), 404

    if 'hints_usados' not in session:
        session['hints_usados'] = {}

    hint_key = f"{obj_id}-nivel{nivel}"

    if hint_key in session['hints_usados']:
        return jsonify({
            "contenido": session['hints_usados'][hint_key],
            "coste": 0,
            "ya_usado": True
        })

    if hint['coste'] > 0:
        total_puntos = sum(v['puntos'] for v in session.get('progreso', {}).values())
        hints_gastados = sum(
            h['coste'] for h in session['hints_usados'].values()
            if isinstance(h, dict) and 'coste' in h
        )
        puntos_disponibles = total_puntos - hints_gastados
        if puntos_disponibles < hint['coste']:
            return jsonify({"error": f"Puntos insuficientes. Necesitas {hint['coste']} pts."}), 403

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hint_path = os.path.join(base_dir, 'scenarios', 'sc-001-ransomware', 'hints', hint['archivo'])

    try:
        with open(hint_path, 'r', encoding='utf-8') as f:
            contenido = f.read().strip()
    except FileNotFoundError:
        return jsonify({"error": "Archivo de hint no encontrado"}), 404

    session['hints_usados'][hint_key] = contenido
    session.modified = True

    return jsonify({
        "contenido": contenido,
        "coste": hint['coste'],
        "nivel": nivel,
        "ya_usado": False
    })


@app.route('/logs/<scenario_id>')
def ver_logs(scenario_id):
    import json as json_module
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logs_path = os.path.join(base_dir, 'scenarios', 'sc-001-ransomware', 'logs', 'events.json')

    try:
        with open(logs_path, 'r', encoding='utf-8') as f:
            eventos = json_module.load(f)
    except FileNotFoundError:
        eventos = []

    return render_template('logs.html', eventos=eventos, scenario_id=scenario_id)


@app.route('/tickets/<scenario_id>')
def tickets(scenario_id):
    sc = next((s for s in SCENARIOS if s['id'] == scenario_id), None)
    if sc is None:
        return "Escenario no encontrado", 404
    return render_template('tickets.html', scenario=sc, tickets=sc.get('tickets', []))


@app.route('/ticket/accion/<scenario_id>/<ticket_id>/<accion_id>', methods=['POST'])
def ticket_accion(scenario_id, ticket_id, accion_id):
    sc = next((s for s in SCENARIOS if s['id'] == scenario_id), None)
    if sc is None:
        return jsonify({"error": "Escenario no encontrado"}), 404

    ticket = next((t for t in sc.get('tickets', []) if t['id'] == ticket_id), None)
    if ticket is None:
        return jsonify({"error": "Ticket no encontrado"}), 404

    accion = next((a for a in ticket['acciones'] if a['id'] == accion_id), None)
    if accion is None:
        return jsonify({"error": "Accion no encontrada"}), 404

    if 'tickets_resueltos' not in session:
        session['tickets_resueltos'] = {}

    ticket_key = f"{scenario_id}-{ticket_id}"
    if ticket_key in session['tickets_resueltos']:
        return jsonify({"error": "Ticket ya cerrado", "ya_resuelto": True})

    session['tickets_resueltos'][ticket_key] = {
        "accion_id": accion_id,
        "correcto": accion['correcto'],
        "puntos": accion['puntos']
    }
    session.modified = True

    return jsonify({
        "correcto": accion['correcto'],
        "feedback": accion['feedback'],
        "puntos": accion['puntos'],
        "impacto": accion['impacto']
    })

@app.route('/evidence/<scenario_id>')
def evidence(scenario_id):
    import json as json_module
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    evidence_path = os.path.join(base_dir, 'scenarios', 'sc-001-ransomware', 'evidence', 'srv-backup01-raw.log')

    try:
        with open(evidence_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except FileNotFoundError:
        contenido = "Archivo de evidencia no encontrado."

    return render_template('evidence.html', contenido=contenido, scenario_id=scenario_id)

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/phishing')
def phishing():
    return render_template('phishing.html')

@app.route('/api/phishing/guardar', methods=['POST'])
def guardar_phishing():
    data = request.get_json()
    if 'phishing_progreso' not in session:
        session['phishing_progreso'] = {}
    
    ticket_id = data.get('ticket_id')
    tab_id = data.get('tab_id')
    pregunta_id = data.get('pregunta_id')
    opcion_id = data.get('opcion_id')

    if ticket_id not in session['phishing_progreso']:
        session['phishing_progreso'][ticket_id] = {}
    if tab_id not in session['phishing_progreso'][ticket_id]:
        session['phishing_progreso'][ticket_id][tab_id] = {}

    session['phishing_progreso'][ticket_id][tab_id][pregunta_id] = opcion_id
    session.modified = True

    return jsonify({"ok": True})

@app.route('/api/phishing/progreso')
def progreso_phishing():
    return jsonify(session.get('phishing_progreso', {}))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)