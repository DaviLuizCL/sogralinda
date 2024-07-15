from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail, Message
import os
secret_key = os.getenv('SECRET_KEY')
if secret_key is None:
    raise ValueError("Problemas com a variável de ambiente - SECRET KEY")

salt_email = os.getenv('SECURITY_SALT')
if salt_email is None:
    raise ValueError("Problemas com a variável de ambiente - SECURITY_SALT")

email_pass = os.getenv('EMAIL_PASS')
if email_pass is None:
    raise ValueError("Problemas com a variável de ambiente - EMAIL_PASS")

email = os.getenv('EMAIL')
if email_pass is None:
    raise ValueError("Problemas com a variável de ambiente - EMAIL")

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key
app.config['SECURITY_PASSWORD_SALT'] = salt_email
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sogrilda.db'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = email
app.config['MAIL_PASSWORD'] = email_pass

app.config['MAIL_DEFAULT_SENDER'] = email

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)

login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça Login para acessar a página'
login_manager.login_message_category = 'alert-info'

from UnhasECafe import routes

#Eu tenho que desenrolar esse bglh do email