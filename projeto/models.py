from projeto import db, login_manager
from projeto import bcrypt
from flask_login import UserMixin
import base64

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def default_profile_photo():
    default_profile_photo = open('projeto/default_profile_photo/default_profile_photo.png', 'rb').read()
    default_profile_photo_decoded = base64.b64encode(default_profile_photo).decode('ascii')
    return default_profile_photo_decoded


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(length=30), nullable=False, unique=True)
    usuario = db.Column(db.String(length=50), nullable=False, unique=True)
    email = db.Column(db.String(length=100), nullable=False, unique=True)
    senha = db.Column(db.String(length=15), nullable=False, unique=True)
    bio = db.Column(db.String(length=1024))
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    perfil_photo = db.Column(db.Text, nullable=False, default=default_profile_photo)
    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)  # Novo campo para rastrear o status de confirmação do e-mail
    email_confirm_token = db.Column(db.String(100), unique=True)  # Novo campo para armazenar o token de confirmação de e-mail
    posts = db.relationship('Posts', backref='dono_user', lazy=True)
    uploads = db.relationship('Uploads', backref='dono_user', lazy=True)
    comentarios = db.relationship('Comments', backref='dono_user', lazy=True)

    def add_perfil_photo(self, data):
        self.perfil_photo = data
        db.session.commit()

    def add_bio(self, desc):
        self.bio = desc
        db.session.commit()

    def add_usuario(self, usuario):
        self.usuario = usuario
        db.session.commit()

    def add_nova_senha(self, senha):
        self.senhacrip = senha
        db.session.commit()
    
    def add_novo_email(self, novo_email):
        self.email = novo_email
        db.session.commit()

    @property
    def senhacrip(self):
        return self.senhacrip
    
    # Faz o set do atributo senhacrip. Ele criptografa a senha para que ela seja inserida no banco de forma segura.
    @senhacrip.setter
    def senhacrip(self, senha_texto):
        self.senha = bcrypt.generate_password_hash(senha_texto).decode('utf-8')

    # Converte a senha criptografada para o normal e a compara com uma outra senha. Deve-se chamar esse método ao realizar o login do usuário.
    def converte_senha(self, senha_texto_claro):
        return bcrypt.check_password_hash(self.senha, senha_texto_claro)
    


class Uploads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary, nullable=False)
    usuario = db.Column(db.Integer, db.ForeignKey('user.id'))
    upload_date = db.Column(db.DateTime(timezone=True), nullable=False)
    string_data = db.Column(db.Text, nullable=False)

    def insert_logged_user_id(self, user_logged):
        self.usuario = user_logged.id
        db.session.commit()


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.Text, nullable=False)
    desc =  db.Column(db.String(length=1024))
    quant_curtidas = db.Column(db.Integer, default=0)
    data_postagem = db.Column(db.DateTime(timezone=True), nullable=False)
    usuario = db.Column(db.Integer, db.ForeignKey('user.id'))
    curtidas = db.relationship('Likes', backref='like_user', lazy=True)
    comentarios = db.relationship('Comments', backref='com_user', lazy=True)

    def curtir(self):
        self.quant_curtidas += 1
        db.session.commit()

    def insert_logged_user_id(self, user_logged):
        self.usuario = user_logged.id
        db.session.commit()

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    usuario = db.Column(db.String(length=50), nullable=False)
    post = db.Column(db.Integer, db.ForeignKey('posts.id'))


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.Integer, db.ForeignKey('user.id'))
    comentario = db.Column(db.String(length=1024), nullable=False)
    post = db.Column(db.Integer, db.ForeignKey('posts.id'))
    data_do_comentario = db.Column(db.DateTime(timezone=True), nullable=False)

    def insert_logged_user_id(self, user_logged):
        self.usuario = user_logged.id
        db.session.commit()
    