from projeto import app
from projeto import db
from projeto.validators import validate_email, validate_senha, validate_usuario
from projeto.models import User, Uploads
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':

        nome = request.form.get('nome')
        usuario = request.form.get('usuario')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirma_senha = request.form.get('confirmar_senha')

        if validate_email(email) and validate_usuario(usuario) and validate_senha(senha):
            if senha == confirma_senha:
                user = User(nome=nome,
                            usuario=usuario,
                            email=email,
                            senhacrip=senha)
                
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
        else:
            flash('Erro ao cadastrar', category='danger')

    return render_template('signup.html')


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        user_logged = User.query.filter_by(email=email).first()
        
        if user_logged and user_logged.converte_senha(senha_texto_claro=senha):
            login_user(user_logged)
            return redirect(url_for('pictures_add'))
        else:
            flash('Erro ao logar', category='danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")
    
@app.route('/pictures_add')
@login_required
def pictures_add():
    return render_template("pictures_add.html")  

@app.route('/perfil/<user>')
@login_required
def perfil(user):
    profile = User.query.filter_by(id=user).first()
    return render_template("perfil.html", profile=profile)

@app.route('/gallery')
@login_required
def gallery():
    return render_template("gallery.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/users')
def users():
    users = User.query.all()
    return render_template("users.html", users=users)
    
