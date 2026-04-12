from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blueforge.db'

db = SQLAlchemy(app)

@app.route('/')
def dashboard():
    return "BlueForge — Panel operativo"

@app.route('/health')
def health():
    return jsonify({"status": "online", "platform": "BlueForge"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)