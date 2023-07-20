from projeto.models import User


def validate_usuario(self, check_user):
    user = User.query.filter_by(usuario=check_user.data).first()
    if user:
        return False
    else:
        return True

def validate_email(self, check_email):
    email = User.query.filter_by(email=check_email.data).first()
    if email:
        return False
    else:
        return True

def validate_senha(self, check_senha):
    senha = User.query.filter_by(senha=check_senha.data).first()
    if senha:
        return False
    else:
        return True
