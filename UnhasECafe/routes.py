from flask import render_template, url_for, redirect, flash, request, session
from UnhasECafe import app, database, bcrypt
from UnhasECafe.forms import FormLogin, FormCriarConta, FormCliente, FormUnha
from UnhasECafe.models import Usuario, Unha
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
    unhas = Unha.query.all()
    if nome == None:
        flash('Nos diga seu nome!', 'alert-info')
        return redirect(url_for('home'))
    return render_template('unhas.html', nome=nome, unhas=unhas)



@app.route('/register_nail', methods=['GET', 'POST'])
@login_required
def cadastro_unhas():
    form_unha = FormUnha()
    if request.method == 'POST':
            unha = Unha(foto=form_unha.foto.data,tipo=form_unha.tipo.data,modelo=form_unha.modelo.data,cor_dominante=form_unha.cor_dominante.data,cor_secundaria=form_unha.cor_secundaria.data,descricao=form_unha.descricao.data,manicure=current_user)
            database.session.add(unha)
            database.session.commit()
            print('Alteração no banco de dados')
            flash(f'Unha adicionada com sucesso', 'alert-success')
            print('Unha criado')
            return redirect(url_for('unhas'))

    return render_template('register_nail.html', form_unha=form_unha)