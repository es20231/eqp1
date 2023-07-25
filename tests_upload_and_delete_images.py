import unittest
import io
from projeto import app, db, allowed_extensions
from projeto.models import User, Uploads
from flask_login import current_user


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.db = db

        # Criando um Banco de Dados SQLite in-memory
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_allowed_extensions(self):
        valid_extensions = ['png', 'jpg', 'jpeg', 'gif']
        for ext in valid_extensions:
            filename = f'test_image.{ext}'
            self.assertTrue(allowed_extensions(filename))
            if ext not in valid_extensions:
                filename = f'test_file.{ext}'
                self.assertFalse(allowed_extensions(filename))
    

    def test_upload_image(self):
        with app.app_context():
            # Cadastrando um usuário de teste
            test_user = User(nome='Test User', usuario='testuser', email='test@example.com', senhacrip='password')
            db.session.add(test_user)
            db.session.commit()

            # Login do usuário de teste
            response = self.app.post('/', data={
                'email': 'test@example.com',
                'senha': 'password'
            }, follow_redirects=True)

            # Verificar se o usuário está logado corretamente
            self.assertEqual(response.status_code, 200)

            # Realizando o upload da imagem por meio da realização de um método POST.
            image_path = 'test_images/test_image.gif' 
            with open(image_path, 'rb') as image_file:
                data = {'image': (image_file, 'test_images/test_image.gif')}
                response = self.app.post('/gallery', data=data, follow_redirects=True)

            # Checando se o status code da resposta HTTP foi 200
            self.assertEqual(response.status_code, 200)

            # Checando se a mensagem flash de sucesso foi retornada
            self.assertIn(b'Imagem cadastrada com sucesso', response.data)

            # Checando se a imagem foi salva no banco de dados
            uploaded_image = Uploads.query.filter_by(usuario=test_user.id).first()
            self.assertIsNotNone(uploaded_image)

    def test_upload_invalid_image_extension(self):
        with app.app_context():
            # Cadastrando um usuário de teste
            test_user = User(nome='Test User', usuario='testuser', email='test@example.com', senhacrip='password')
            db.session.add(test_user)
            db.session.commit()

            # Login do usuário de teste
            response = self.app.post('/', data={
                'email': 'test@example.com',
                'senha': 'password'
            }, follow_redirects=True)

            # Verificar se o usuário está logado corretamente
            self.assertEqual(response.status_code, 200)

            # Realizar o upload de imagem de formato inválido
            with open('test_images/test_file.txt', 'rb') as invalid_image_file:
                data = {'image': (invalid_image_file, 'test_images/test.file.txt')}
                response = self.app.post('/gallery', data=data, follow_redirects=True)

            # Verificando se a resposta contém a mensagem de erro esperada
            error_message = 'Utilize um tipo de arquivo compatível (png, jpg, jpeg, gif)'
            self.assertIn(error_message.encode('utf-8'), response.data)

            # Checando se a imagem não foi salva no banco de dados
            uploaded_image = Uploads.query.filter_by(usuario=test_user.id).first()
            self.assertIsNone(uploaded_image)
    
    def test_upload_no_image(self):
        with app.app_context():
            # Cadastrando um usuário de teste
            test_user = User(nome='Test User', usuario='testuser', email='test@example.com', senhacrip='password')
            db.session.add(test_user)
            db.session.commit()

            # Login do usuário de teste
            response = self.app.post('/', data={
                'email': 'test@example.com',
                'senha': 'password'
            }, follow_redirects=True)

            # Verificar se o usuário está logado corretamente
            self.assertEqual(response.status_code, 200)

            # Verificar se nenhuma imagem foi indentificada
            no_file = []
            data = {
                'image' : (no_file, '')
            }
            response = self.app.post('/gallery', data= data, follow_redirects = True)

            # Verificar se a checagem contém a mensagem de erro esperada
            error_message = "Nenhum arquivo foi selecionado"
            self.assertIn(error_message.encode('utf-8'), response.data)

            # Checando se a imagem não foi salva no banco de dados
            uploaded_image = Uploads.query.filter_by(usuario=test_user.id).first()
            self.assertIsNone(uploaded_image)

    def test_delete_image(self):
        with app.app_context():
            # Cadastrando um usuário de teste
            test_user = User(nome='Test User', usuario='testuser', email='test@example.com', senhacrip='password')
            db.session.add(test_user)
            db.session.commit()

            # Login do usuário de teste
            response = self.app.post('/', data={
                'email': 'test@example.com',
                'senha': 'password'
            }, follow_redirects=True)

            # Verificar se o usuário está logado corretamente
            self.assertEqual(response.status_code, 200)

            # Criando uma imagem de teste ao usuário de teste
            test_image_data = b'test_images/test_image.gif'
            test_image = Uploads(data=test_image_data)
            db.session.add(test_image)
            db.session.commit()
            test_image.insert_logged_user_id(test_user)
            # Verificar se a imagem está no banco de dados
            uploaded_image = Uploads.query.filter_by(usuario=test_user.id).first()
            self.assertIsNotNone(uploaded_image)

            # Realizar a remoção da imagem por meio do envio de um GET para a rota 'delete_image'
            response = self.app.get(f'{uploaded_image.id}/gallery', follow_redirects=True)

            # Verificar se a mensagem de resposta é 200
            self.assertEqual(response.status_code, 200)

            # Verificar se a mensagem flash de sucesso foi retornada
            self.assertIn(b"Imagem removida com sucesso", response.data)

            # Verificar se a imagem foi realmente deletada do banco de dados
            deleted_image = Uploads.query.filter_by(usuario=test_user.id).first()
            self.assertIsNone(deleted_image)

if __name__ == '__main__':
    unittest.main()