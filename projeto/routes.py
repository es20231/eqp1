from projeto import app
from projeto import db
from projeto.validators import validate_email, validate_senha, validate_usuario
from projeto.models import User
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/', methods=['POST', 'GET'])
def page_home():
    return 'HelloWorld'


@app.route('/register', methods=['POST', 'GET'])
def page_register():
    if request.method == 'POST':

        nome = request.form['nome']
        usuario = request.form['usuario']
        email = request.form['email']
        senha = request.form['senha']

        if validate_usuario(usuario) and validate_email(email) and validate_senha(senha):
            user = User(nome, usuario, email, senha)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('page_login'))
        
        else:
            flash('Erro ao cadastrar', category='danger')

    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def page_login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user_logged = User.query.filter_by(email=email).first()
        
        if user_logged and user_logged.converte_senha(senha_texto_claro=senha):
            return redirect(url_for('page_home'))
        else:
            flash('Erro ao logar', category='danger')

    return render_template('login.html')


@app.route('/logout')
def page_logout():
    logout_user()
    return redirect(url_for('login'))