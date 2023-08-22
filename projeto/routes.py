from projeto import app
from projeto import db
from projeto import serializer
from projeto import mail
from projeto import allowed_extensions
from projeto.validators import validate_email, validate_senha, validate_usuario
from projeto.models import User, Uploads, Posts, Comments, Likes_Dislikes, Likes_Comments
from flask import render_template, redirect, request, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
import base64
from flask_mail import Mail, Message
from sqlalchemy import desc
from datetime import datetime
from werkzeug.exceptions import RequestEntityTooLarge
from projeto.filters import *


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
                # Gerar um token para o usuário
                token = serializer.dumps({'email': email}, salt='email-confirm')
                user = User(nome=nome,
                            usuario=usuario,
                            email=email,
                            date_created = datetime.now().replace(microsecond=0),
                            senhacrip=senha,
                            email_confirm_token=token,  # Armazene o token no campo do usuário
                            email_confirmed=False)  # Defina o status de confirmação como falso até que o e-mail seja confirmado
                # user.email_confirm_token = token  # Armazena o token no campo do usuário
                # user.email_confirmed = False  # Definir o status de confirmação como falso até que o e-mail seja confirmado

                db.session.add(user)
                db.session.commit()

                # Enviar o e-mail de confirmação
                msg = Message('Confirme seu registro',
                              recipients=[email])
                link = url_for('confirm_email', token=token, _external=True)
                msg.html = render_template("registration.html", link=link)
                mail.send(msg)
                
                

                flash('Um e-mail de confirmação foi enviado. Por favor, verifique sua caixa de entrada.', category='success')
                return redirect(url_for('login'))
                
        else:
            flash('Erro ao cadastrar, tente novamente', category='danger')

    return render_template('signup.html')


# Rota para confirmar o e-mail
@app.route('/confirm_email/<token>')
def confirm_email(token):
    
    try:
        # Decodificar o token para verificar o valor
        decoded_token = serializer.loads(token, salt='email-confirm', max_age=3600)
        print("Decoded token:", decoded_token)

        # Recuperar o email do token decodificado
        email = decoded_token.get('email', None)
        print("Decoded email:", email)

        if email:
            user = User.query.filter_by(email=email).first()
            print("User:", user)

            if user:
                user.email_confirmed = True
                user.email_confirm_token = None
                db.session.commit()
                flash('E-mail confirmado com sucesso. Você pode fazer login agora.', category='success')
                msg = Message('Conta confirmada!', recipients=[user.email])
                msg.html = render_template("confirm_registration.html", user=user)
                mail.send(msg)
            else:
                flash('Erro ao confirmar e-mail. Usuário não encontrado.', category='danger')
        else:
            flash('Erro ao confirmar e-mail. Email não encontrado no token decodificado.', category='danger')

    except Exception as e:
        flash('Erro ao confirmar e-mail. Por favor, tente novamente.', category='danger')

    return redirect(url_for('login'))


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        user_logged = User.query.filter_by(email=email).first()
        
        if user_logged and user_logged.converte_senha(senha_texto_claro=senha):
            if user_logged.email_confirmed:
                login_user(user_logged)
                return redirect(url_for('feed', id=user_logged.id))
            else:
                flash('Erro ao logar, confirme sua conta!', category='danger')
                return redirect(request.url)
        else:
            flash("Erro ao logar, email ou senha invalidos!", category="danger")
            return redirect(request.url)

    return render_template('login.html')


@app.route('/registration')
def registration():
    return render_template("registration.html")


@app.route('/confirm_registration')
def confirm_registration():
    return render_template("confirm_registration.html")


@app.route('/token_expired')
def token_expired():
    return render_template("token_expired.html")


@app.route('/password_recovery', methods=['GET', 'POST'])
def password_recovery():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            # Gerar um token para a redefinição de senha
            token = serializer.dumps({'email': email}, salt='password-reset')

            # Enviar o email de redefinição de senha
            msg = Message('Redefinição de Senha',
                          recipients=[email],
                          sender='microgram84@gmail.com')
            link = url_for('password_redefinition', token=token, _external=True)
            msg.body = f'Clique no link a seguir para redefinir sua senha: {link}'
            mail.send(msg)

            flash('Um email de redefinição de senha foi enviado. Por favor, verifique sua caixa de entrada.', category='success')
            return redirect(url_for('login'))
        else:
            flash('O email fornecido não corresponde a nenhum usuário.', category='danger')
            return redirect(url_for('login'))

    return render_template('password_recovery.html')


@app.route('/password_redefinition/<token>', methods=['GET', 'POST'])
def password_redefinition(token):
    try:
        decoded_token = serializer.loads(token, salt='password-reset', max_age=3600)
        email = decoded_token.get('email', None)
        user = User.query.filter_by(email=email).first()

        if request.method == 'POST':
            nova_senha = request.form.get('nova_senha')
            confirma_senha = request.form.get('confirmar_senha')

            if nova_senha == confirma_senha:
                user.senhacrip = nova_senha  # Atualizar a senha do usuário
                user.email_confirmed = True  # Defina o status de confirmação como True
                db.session.commit()

                flash('Senha redefinida com sucesso. Você pode fazer login agora.', category='success')
                return redirect(url_for('login'))
            else:
                flash('As senhas digitadas não correspondem.', category='danger')

    except Exception as e:
        flash('Erro ao redefinir senha. Por favor, tente novamente.', category='danger')

    
    return render_template("password_redefinition.html", token=token)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")
    
@app.route('/perfil/<int:id>/feed')
@login_required
def feed(id):
    all_posts = Posts.query.order_by(desc(Posts.data_postagem)).all()
    all_comments = Comments.query.order_by(desc(Comments.data_do_comentario)).all()
    all_user_likes_dislikes = Likes_Dislikes.query.filter_by(usuario=id).all()
    all_user_comments_likes = Likes_Comments.query.filter_by(usuario=id).all()
    return render_template("pictures_add.html", posts= all_posts, comentarios=all_comments, likes_dislikes=all_user_likes_dislikes, all_user_comments_likes = all_user_comments_likes)  

@app.route('/perfil/<int:id>/feed/post/<int:image_id>', methods=["POST"])
@login_required
def postar_foto(id,image_id):
    if request.method == "POST":
        legenda_post = request.form.get('legenda')
        selected_filter = request.form.get('selected_filter')

        imagem_post = Uploads.query.filter_by(id=image_id).first()
        if imagem_post.data == '':
            flash('Imagem não registrada na galeria. Faça upload da imagem na galeria para depois realizar a postagem.', "feed_post_image_error")
            return redirect(request.url)
        else:
            if selected_filter == 'Preto e Branco':
                imagem_filtrada = apply_filter(imagem_post.data,black_and_white_filter)
                new_post = Posts(data=imagem_filtrada,desc=legenda_post, data_postagem=datetime.now())
                db.session.add(new_post)
                db.session.commit()
                new_post.insert_logged_user_id(current_user)
                flash("Postagem realizada com sucesso.", "success_post")
                return redirect(url_for('feed', id=current_user.id))
            elif selected_filter == 'Desfoque':
                imagem_filtrada = apply_filter(imagem_post.data,blur_filter)
                new_post = Posts(data=imagem_filtrada,desc=legenda_post, data_postagem=datetime.now())
                db.session.add(new_post)
                db.session.commit()
                new_post.insert_logged_user_id(current_user)
                flash("Postagem realizada com sucesso.", "success_post")
                return redirect(url_for('feed', id=current_user.id))
            else:
                new_post = Posts(data=imagem_post.string_data,desc=legenda_post, data_postagem=datetime.now())
                db.session.add(new_post)
                db.session.commit()
                new_post.insert_logged_user_id(current_user)
                flash("Postagem realizada com sucesso.", "success_post")
                return redirect(url_for('feed', id=current_user.id))

    return redirect(request.url)

@app.route('/excluir_post', methods=["POST"])
@login_required
def excluir_post():
    if request.method == 'POST':
        post_id = request.args.get('post_id')

        post_relacionado = Posts.query.filter_by(id=post_id,usuario=current_user.id).first()
        if post_relacionado:
            comentarios_post = Comments.query.filter_by(post=post_relacionado.id).all()
            likes_dislikes_post = Likes_Dislikes.query.filter_by(post=post_relacionado.id).all()
            comments_likes_post = Likes_Comments.query.filter_by(post_id = post_relacionado.id).all()

            for like in comments_likes_post:
                db.session.delete(like)
                db.session.commit()

            for like_dislike in likes_dislikes_post:
                db.session.delete(like_dislike)
                db.session.commit()
            
            for comentario in comentarios_post:
                db.session.delete(comentario)
                db.session.commit()
            
            has_remaining_comments_likes = Likes_Comments.query.filter_by(post_id=post_relacionado.id).all()
            has_remaining_comments = Comments.query.filter_by(post= post_relacionado.id).all()
            has_remaining_likes_dislikes = Likes_Dislikes.query.filter_by(post=post_relacionado.id).all()

            if not has_remaining_comments_likes:
                if not has_remaining_likes_dislikes:
                    if not has_remaining_comments:
                        db.session.delete(post_relacionado)
                        db.session.commit()
                        return redirect(url_for('feed', id=current_user.id))
            
            else:
                flash('Erro ao tentar excluir uma postagem.Tente novamente', "error_delete_post")
                return redirect(request.url)
    return redirect(request.url)

@app.route('/<string:nome>/realizar_comentario/post/<string:nome_user_post>/<int:post_id>', methods=["GET","POST"])
@login_required
def comentar_post(nome,nome_user_post,post_id):
    if request.method == "POST":
        comentario = request.form.get('comentario')
        
        if comentario == '':
            flash('Campo de comentário deve ser preenchido', 'empy_comment_error')
            return redirect(request.url)
        else:
            new_comment = Comments(comentario=comentario, post=post_id, data_do_comentario=datetime.now())
            db.session.add(new_comment)
            db.session.commit()
            new_comment.insert_logged_user_id(current_user)
            return redirect(url_for('feed', id=current_user.id))
    
    return redirect(url_for('feed', id=current_user.id))

@app.route('/registrar_like_dislike', methods=["POST"])
@login_required
def registrar_like_dislike():
    if request.method == "POST":
        action = request.args.get('action')
        post_id = int(request.args.get('post_id'))

        post_relacionado = Posts.query.filter_by(id=post_id).first()

        if post_id != post_relacionado.id:
            return jsonify({"error": 'Post não encontrado'}), 404
        
        has_like_dislike = Likes_Dislikes.query.filter_by(post= post_id, usuario=current_user.id).first()
        if has_like_dislike:
            post = Posts.query.filter_by(id=post_id).first()
            if action == 'like':
                if has_like_dislike.value == 0:
                    has_like_dislike.value = 1
                    db.session.commit()
                    post.quant_dislikes -= 1
                    db.session.commit()
                    post.quant_likes += 1
                    db.session.commit()
                    return redirect(url_for('feed', id=current_user.id))
                
                elif has_like_dislike.value == 1:
                    has_like_dislike.value = 1
                    db.session.commit()
                    return redirect(url_for('feed', id=current_user.id))

            elif action == 'dislike':
                if has_like_dislike.value == 0:
                    has_like_dislike.value = 0
                    db.session.commit()
                    return redirect(url_for('feed', id=current_user.id))
                
                elif has_like_dislike.value == 1:
                    has_like_dislike.value = 0
                    db.session.commit()
                    post.quant_likes -= 1
                    db.session.commit()
                    post.quant_dislikes += 1
                    db.session.commit()
                    return redirect(url_for('feed', id=current_user.id))
            

        else:
            if action == 'like':
                new_like = Likes_Dislikes(post = post_id, value = 1)
                db.session.add(new_like)
                db.session.commit()
                new_like.insert_logged_user_id(current_user)

                post = Posts.query.filter_by(id=post_id).first()
                post.curtir()
                return redirect(url_for('feed', id=current_user.id))
            
            elif action == 'dislike':
                new_dislike = Likes_Dislikes(post=post_id, value = 0)
                db.session.add(new_dislike)
                db.session.commit()
                new_dislike.insert_logged_user_id(current_user)

                post = Posts.query.filter_by(id=post_id).first()
                post.descurtir()
                return redirect(url_for('feed', id=current_user.id))
    return redirect(request.url)

@app.route('/registrar_like_comment', methods=["POST"])
@login_required
def registrar_like_comentario():
    if request.method == "POST":
        action = request.args.get('action')
        post_id = int(request.args.get('post_id'))
        comment_id = int(request.args.get('comment_id'))

        post_relacionado = Posts.query.filter_by(id=post_id).first()

        if post_relacionado.id == post_id:
            comentario_do_post = Comments.query.filter_by(id=comment_id,post=post_id).first()

            if not comentario_do_post:
                return jsonify({"error": 'Comentário não encontrado'}), 404
            
            has_like = Likes_Comments.query.filter_by(post_id=post_id, usuario=current_user.id,comentario_id=comment_id).first()
            if has_like:
                if action == 'like':
                    if has_like.value == 1:
                        has_like.value = 1
                        db.session.commit()
                        return redirect(url_for('feed', id=current_user.id))
                    
                    elif has_like.value == 0:
                        has_like.value = 1
                        db.session.commit()
                        comentario_do_post.quant_likes += 1
                        db.session.commit()
                        return redirect(url_for('feed', id=current_user.id))
            
            else:
                if action == 'like':
                    new_like_comment = Likes_Comments(comentario_id = comment_id, post_id=post_id, value = 1)
                    db.session.add(new_like_comment)
                    db.session.commit()
                    new_like_comment.insert_logged_user_id(current_user)

                    comentario = Comments.query.filter_by(id=comment_id,post=post_id).first()
                    comentario.curtir_comentario()
                    return redirect(url_for('feed', id=current_user.id))
        else:
            return jsonify({"error": "Post não encontrado"}), 404

    return redirect(request.url)

@app.route('/perfil/<user>')
@login_required
def perfil(user):
    total_contas = 0
    total_profiles = User.query.all()
    for conta in total_profiles:
        total_contas +=1
    profile = User.query.filter_by(id=user).first()
    posts = Posts.query.filter_by(usuario=user).all()
    return render_template("perfil.html", profile=profile, user_posts = posts, total_users = total_contas)

@app.route('/gallery')
@login_required
def gallery():
    page = request.args.get("page", 1, type=int)
    per_page = 5
    all_images = Uploads.query.filter_by(usuario=current_user.id).order_by(desc(Uploads.upload_date)).paginate(page=page, per_page=per_page)
    return render_template("gallery.html", pagination = all_images)

@app.errorhandler(RequestEntityTooLarge)
def handle_request_entity_too_large(e):
    flash("O arquivo é muito grande. O tamanho máximo permitido é de 20 MB por upload.", "file_length_error")
    return redirect(request.url)

@app.route('/gallery', methods=["POST"])
@login_required
def upload_image():
    if request.method == 'POST':
        photos = request.files.getlist('images[]')

        for photo in photos:
            if photo.filename == '':
                flash("Nenhum arquivo foi selecionado", category="file_error")
                return redirect(request.url)
            
            if not allowed_extensions(photo.filename):
                flash("Utilize um tipo de arquivo compatível (png, jpg, jpeg, gif)", category="compatibility_error")
                return redirect(request.url)
            

            blob_photo = photo.read()
            blob_photo_decoded = base64.b64encode(blob_photo).decode('ascii')
            new_photo = Uploads(data=blob_photo, string_data=blob_photo_decoded,upload_date=datetime.now())
            db.session.add(new_photo)
            db.session.commit()
            new_photo.insert_logged_user_id(current_user)

        if len(photos) > 1:
            flash("Imagens cadastradas com sucesso", category="upload_success")
        elif len(photos) == 1:
            flash("Imagem cadastrada com sucesso", category="upload_success")
        return redirect(url_for('gallery'))

    return redirect(request.url)

@app.route('/<int:id>/gallery')
@login_required
def delete_image(id):
    image = Uploads.query.filter_by(id=id).first()
    db.session.delete(image)
    db.session.commit()
    flash("Imagem removida com sucesso", category="delete_success")
    return redirect(url_for('gallery'))
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template("users.html", users=users)
    

@app.route('/configuration', methods=['POST', 'GET'])
@login_required
def configuration():

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        bio = request.form.get('biografia')
        email = request.form.get('email')
        senha = request.form.get('senha')
        nova_senha = request.form.get('nova_senha')
        novo_email = request.form.get('novo_email')
        if usuario:
            current_user.add_usuario(usuario)
        if bio:
            current_user.add_bio(bio)
        if novo_email:
            current_user.add_novo_email(novo_email)
        if email and senha and nova_senha:
            if current_user.converte_senha(senha_texto_claro=senha) and not validate_email(email):
                current_user.add_nova_senha(nova_senha)
                flash('Senha alterada. Logue novamente na sua conta.', category="success")
                return redirect(url_for('logout'))
            else:
                flash('Erro ao alterar senha: Email ou Senha fornecidos inválidos', category='danger')
                return redirect(url_for('configuration'))
        return redirect(url_for('perfil', user=current_user.id))
    

    return render_template('configuration.html', user=current_user)

@app.route('/configuration_user_profile_photo', methods=["POST"])
@login_required
def profile_photo_configuration():
    photo = request.files['image']
    if photo.filename != '':
            if not allowed_extensions(photo.filename):
                flash("Utilize um tipo de arquivo compatível (png, jpg, jpeg, gif)", category="compatibility_error")
                return redirect(request.url)
            else:
                blob_photo = photo.read()
                blob_photo_decoded = base64.b64encode(blob_photo).decode('ascii')
                current_user.add_perfil_photo(blob_photo_decoded)
                return redirect(url_for('perfil', user=current_user.id))
    
    return render_template('configuration.html', user=current_user)
