from flask import render_template, url_for, redirect, flash, request, session
from UnhasECafe import app, database, bcrypt, mail
from UnhasECafe.forms import FormLogin, FormCriarConta, FormCliente, FormUnha
from UnhasECafe.models import Usuario, Unha
from UnhasECafe.decorators import check_is_confirmed
from flask_login import login_user, logout_user, current_user, login_required
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from datetime import datetime
import urllib.parse
import secrets
import os
import re
from PIL import Image

def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_SALT"])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration)
        return email
    except Exception:
        return False

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config["MAIL_DEFAULT_SENDER"],
    )
    mail.send(msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    print(request.form)
    if request.method == 'POST':
        if form.validate_on_submit() and 'botao_submit_login' in request.form:
            if '@' in form.user.data:
                usuario = Usuario.query.filter_by(email=form.user.data).first()
            else:
                usuario = Usuario.query.filter_by(telefone=form.user.data).first()
            
            if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
                login_user(usuario)
                flash(f'Login feito com sucesso {usuario.nome}, fique à vontade!', 'alert-success')
                return redirect(url_for('cadastro_unhas'))
            else:
                flash('Usuário ou senha incorretos', 'danger')
                return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = FormCriarConta()
    if request.method == 'POST':
        if form.validate_on_submit() and 'botao_submit_criarconta' in request.form:
            senha_cript = bcrypt.generate_password_hash(form.senha.data)
            #username, nome, email, telefone, senha
            usuario = Usuario(username=form.username.data, email=form.email.data, senha=senha_cript, telefone=form.telefone.data, nome=form.username.data)
            database.session.add(usuario)
            database.session.commit()
            print('Alteração no banco de dados')
            flash(f'Conta criada com sucesso, {form.username.data}, obrigado!', 'alert-success')
            print('usuario criado')

            token = generate_token(usuario.email)
            confirmar_email = url_for('confirm_email', token=token, _external=True)
            html = render_template("confirm_email.html", confirm_url=confirmar_email)
            subject = "Por favor, confirme seu e-mail"
            send_email(usuario.email, subject, html)
            login_user(usuario)
            flash("O e-mail de confirmação foi enviado", "success")
            return redirect(url_for('login'))
    return render_template('cadastro.html', form=form)

@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    if current_user.confirmado:
        flash("Conta já autorizada.", "success")
        return redirect(url_for("home"))
    email = confirm_token(token)
    user = Usuario.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.confirmado = True
        user.confirmed_em = datetime.now()
        database.session.add(user)
        database.session.commit()
        flash("Obrigado por autorizar sua conta!", "success")
    else:
        flash("O token de confirmação é inválido ou expirou, tente novamente", "danger")
    return redirect(url_for("home"))

@app.route('/', methods=['GET', 'POST'])
def home():
    form = FormCliente()
    nome_cliente = form.nome.data
    session['nome'] = nome_cliente
    if request.method == 'POST':
        flash(f'Sinta-se em casa {nome_cliente}, fique à vontade!', 'alert-success')
        return redirect(url_for('unhas'))
    return render_template('home.html', form=form)

@app.route('/unhas', methods=['GET', 'POST'])
def unhas():
    nome = session.get('nome', 'cliente')
    unhas = Unha.query.all()
    if nome is None:
        flash('Nos diga seu nome!', 'alert-info')
        return redirect(url_for('home'))

    return render_template('unhas.html', nome=nome, unhas=unhas)

@app.route('/msg_whats/<tipo>/<modelo>/<cor_dominante>', methods=['GET'])
def msg_whats(tipo, modelo, cor_dominante):
    cliente = session.get('nome', 'cliente')
    msg = f'Oi, sou a {cliente}, gostei da unha tipo {tipo}, no modelo {modelo} na cor {cor_dominante} e gostaria de fazer um orçamento!'
    whatsapp_url = f"https://wa.me/5583998317442?text={urllib.parse.quote(msg)}"
    return redirect(whatsapp_url)

@app.route('/unhas/excluir/<id_unha>', methods=['POST'])
def excluir_unha(id_unha):
    unha = Unha.query.get(id_unha)
    database.session.delete(unha)
    database.session.commit()
    flash('Unha excluída', 'alert-danger')
    return redirect(url_for('unhas'))

def limpar_nome_arquivo(nome):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', nome)

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_limpo = limpar_nome_arquivo(nome)
    nome_completo = nome_limpo + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/imagens', nome_completo)
    
    tamanho = (500, 500)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    
    imagem_reduzida.save(caminho_completo)
    
    # Mensagens de depuração
    print(f'Imagem salva em: {caminho_completo}')
    print(f'Nome completo da imagem: {nome_completo}')
    
    return nome_completo

@app.route('/register_nail', methods=['GET', 'POST'])
@login_required
def cadastro_unhas():
    form_unha = FormUnha()
    if request.method == 'POST':
        if form_unha.foto.data:
            foto_unha = salvar_imagem(form_unha.foto.data)
        unha = Unha(foto=foto_unha, tipo=form_unha.tipo.data, modelo=form_unha.modelo.data, cor_dominante=form_unha.cor_dominante.data, cor_secundaria=form_unha.cor_secundaria.data, descricao=form_unha.descricao.data, manicure=current_user)
        database.session.add(unha)
        database.session.commit()
        print('Alteração no banco de dados')
        flash(f'Unha adicionada com sucesso', 'alert-success')
        print('Unha criada')
        return redirect(url_for('cadastro_unhas'))

    return render_template('register_nail.html', form_unha=form_unha)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso!', 'alert-success')
    return redirect(url_for('home'))
