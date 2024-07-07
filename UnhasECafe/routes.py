from flask import render_template, url_for, redirect, flash, request, session
from UnhasECafe import app, database, bcrypt
from UnhasECafe.forms import FormLogin, FormCriarConta, FormCliente
from UnhasECafe.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required



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
                flash(f'Login feito com sucesso {usuario.nome}, fique à vontade!')
                return redirect(url_for('home'))
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
            usuario = Usuario(username=form.username.data,email=form.email.data,senha=senha_cript, telefone=form.telefone.data, nome=form.username.data)
            database.session.add(usuario)
            database.session.commit()
            print('Alteração no banco de dados')
            flash(f'Conta criada com sucesso, {form.username.data}, obrigado!', 'alert-success')
            print('usuario criado')
            return redirect(url_for('login'))
    return render_template('cadastro.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = FormCliente()
    nome_cliente = form.nome.data
    session['nome'] = nome_cliente
    if request.method == 'POST':
        return redirect(url_for('unhas'))
    return render_template('home.html', form=form)
@app.route('/unhas')
def unhas():
    nome = session.get('nome', 'cliente')
    return render_template('unhas.html', nome=nome)
    


