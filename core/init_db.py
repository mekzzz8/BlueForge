from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blueforge.db'

db = SQLAlchemy(app)

class Scenario(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    empresa = db.Column(db.String(100), nullable=False)
    dificultad = db.Column(db.String(10), nullable=False)
    puntos_max = db.Column(db.Integer, nullable=False)
    completado = db.Column(db.Boolean, default=False)

class Objetivo(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    scenario_id = db.Column(db.String(10), db.ForeignKey('scenario.id'))
    pregunta = db.Column(db.String(300), nullable=False)
    flag = db.Column(db.String(100), nullable=False)
    puntos = db.Column(db.Integer, nullable=False)
    resuelto = db.Column(db.Boolean, default=False)

class Progreso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.String(10), db.ForeignKey('scenario.id'))
    objetivo_id = db.Column(db.String(10), db.ForeignKey('objetivo.id'))
    respuesta = db.Column(db.String(100), nullable=False)
    correcta = db.Column(db.Boolean, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.String(10), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    severidad = db.Column(db.String(10), nullable=False)
    estado = db.Column(db.String(20), default='Abierto')
    accion_tomada = db.Column(db.String(100), nullable=True)
    impacto_negocio = db.Column(db.Integer, default=0)
    fecha_apertura = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_cierre = db.Column(db.DateTime, nullable=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Base de datos BlueForge creada correctamente")