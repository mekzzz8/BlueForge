from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blueforge.db'

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
                "puntos": 150
            },
            {
                "id": "OBJ-002",
                "pregunta": "¿Qué dirección IP externa contactó el malware durante la fase C2?",
                "categoria": "Network Forensics",
                "flag": "185.220.101.47",
                "puntos": 200
            },
            {
                "id": "OBJ-003",
                "pregunta": "¿Qué clave de registro usó el malware para establecer persistencia?",
                "categoria": "Incident Response",
                "flag": "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
                "puntos": 250
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

@app.route('/health')
def health():
    return jsonify({"status": "online", "platform": "BlueForge"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)