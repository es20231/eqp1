from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
import os
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

#GMAIL
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'microgram84@gmail.com'  # Insira seu e-mail do Gmail
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")  # Insira sua senha do Gmail
app.config['MAIL_DEFAULT_SENDER'] = 'microgram84@gmail.com'  # Endereço de e-mail padrão para enviar e-mails
app.config['MAIL_MAX_EMAILS'] = None  # Limite máximo de e-mails por conexão (None para ilimitado)
app.config['MAIL_SUPPRESS_SEND'] = False  # Defina como True para suprimir o envio real de e-mails durante testes

# Permitir acesso a aplicativos menos seguros (Isso pode ser necessário para o Gmail)
# Certifique-se de que essa configuração não seja usada em um ambiente de produção com dados sensíveis.
# É recomendável usar um método de autenticação mais seguro, como OAuth2.
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_PORT'] = 587

mail = Mail(app)

# Configurar o Serializer para gerar tokens seguros
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_extensions(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


from projeto import routes