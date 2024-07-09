from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import os
secret_key = os.getenv('SECRET_KEY')
if secret_key is None:
    raise ValueError("Problemas com a variável de ambiente")

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sogrilda.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça Login para acessar a página'
login_manager.login_message_category = 'alert-info'

from UnhasECafe import routes