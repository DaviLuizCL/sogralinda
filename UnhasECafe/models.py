from UnhasECafe import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True) 
    username = database.Column(database.String, nullable=False)
    nome = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    telefone = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    confirmado = database.Column(database.Boolean, nullable=False, default=False)
    confirmado_em = database.Column(database.DateTime, nullable=True)
    unha = database.relationship('Unha', backref='manicure', lazy=True)

class Unha(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True) 
    foto = database.Column(database.String, nullable=False)
    tipo = database.Column(database.String, nullable=False)
    modelo = database.Column(database.String, nullable=False)
    cor_dominante = database.Column(database.String, nullable=False)
    cor_secundaria = database.Column(database.String, nullable=False)
    descricao = database.Column(database.String, nullable=False)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

