from flask import render_template, url_for, redirect, flash, request, session
from UnhasECafe import app, database, bcrypt
from UnhasECafe.forms import FormLogin, FormCriarConta
from UnhasECafe.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required



@app.route('/', methods=['GET', 'POST'])
def login():
    form = FormLogin()
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

@app.route('/homepage')
def homepage():
    return render_template('home.html')


