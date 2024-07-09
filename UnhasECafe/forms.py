from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import TextArea
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
    user = StringField('E-mail ou Número de telefone', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    botao_submit_login = SubmitField('Fazer Login')

    # def validate_user(self, user):
    #     try:
    #         if not self.is_email(user.data) and not self.is_valid_phone(user.data):
    #             raise ValidationError('Seu usuário deve ser um email ou um número de telefone válido.')
    #     except Exception as e:
    #         raise ValidationError('N entendi oq houve mas to averiguando')
    # def is_email(self, value):
    #     try:
    #         Email().validate_email(value)
    #         return True
    #     except ValidationError:
    #         return False
        
    # def is_valid_phone(self, value):
    #     try:
    #         p = phonenumbers.parse(value)
    #         return phonenumbers.is_valid_number(p)
    #     except phonenumbers.phonenumberutil.NumberParseException:
    #         return False
        
class FormCliente(FlaskForm):
    nome = StringField('Digite seu nome', validators=[DataRequired()])
    botao_nome = SubmitField('Enviar')



class FormUnha(FlaskForm):
    foto = FileField('Foto da unha', validators=[DataRequired()])
    tipo = StringField('Tipo de unha', validators=[DataRequired()])
    modelo = StringField('Modelo da unha', validators=[DataRequired()])
    cor_dominante = StringField('Cor predominante', validators=[DataRequired()])
    cor_secundaria = StringField('Cor secundária', validators=[DataRequired()])
    descricao = StringField('Descrição da unha', widget=TextArea(), validators=[DataRequired()])
    botao_enviar_unha = SubmitField('Enviar')

    
    
    