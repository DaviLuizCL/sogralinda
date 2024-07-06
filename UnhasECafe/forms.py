from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import phonenumbers
from datetime import datetime
from UnhasECafe.models import Usuario

class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre outro e-mail ou faça login para continuar')
    
    def validate_telefone(self, telefone):
        usuario = Usuario.query.filter_by(telefone=telefone.data).first()
        if usuario:
            raise ValidationError('Numero já cadastrado. Cadastre outro Numero de telefone ou faça login para continuar')
        
class FormLogin(FlaskForm):
    user = StringField('E-mail ou Número de telefone', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    botao_submit_login = SubmitField('Fazer Login')

    def validate_user(self, user):
        if not self.is_email(user.data) and not self.is_valid_phone(user.data):
            raise ValidationError('Seu usuário deve ser um email ou um número de telefone válido.')
        
    def is_email(self, value):
        try:
            Email().validate_email(value)
            return True
        except ValidationError:
            return False
        
    def is_valid_phone(self, value):
        try:
            p = phonenumbers.parse(value)
            return phonenumbers.is_valid_number(p)
        except phonenumbers.phonenumberutil.NumberParseException:
            return False
        
