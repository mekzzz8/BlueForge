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
        "desc": "FinCorp Solutions sufre cifrado masivo a las 3AM. Analiza los logs de Windows para reconstruir la cadena de ataque completa."
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

@app.route('/health')
def health():
    return jsonify({"status": "online", "platform": "BlueForge"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)