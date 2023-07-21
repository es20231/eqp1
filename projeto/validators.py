from projeto.models import User


def validate_usuario(check_user):
    user = User.query.filter_by(usuario=check_user).first()
    if user:
        return False
    else:
        return True

def validate_email(check_email):
    email = User.query.filter_by(email=check_email).first()
    if email:
        return False
    else:
        return True

def validate_senha(check_senha):
    senha = User.query.filter_by(senha=check_senha).first()
    if senha:
        return False
    else:
        return True
