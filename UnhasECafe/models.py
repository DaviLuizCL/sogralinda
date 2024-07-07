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

# class SuperUsuario(database.Model, UserMixin):
#     id = database.Column(database.Integer, primary_key=True) 
#     username = database.Column(database.String, nullable=False)
#     email = database.Column(database.String, nullable=False, unique=True)
#     telefone = database.Column(database.String, nullable=False, unique=True)
#     senha = database.Column(database.String, nullable=False)
#     posts = database.relationship('Post', backref='autor', lazy=True)
     
class Unha(database.Model):
    foto = database.Column(database.String, nullable=False)
    cores = database.Column(database.String, nullable=False)
    estilo = database.Column(database.String, nullable=False)
    modelo = database.Column(database.String, nullable=False)
    descricao = database.Column(database.String, nullable=False)