import unittest
from projeto import app, db
from projeto.models import User
from flask_login import login_user, logout_user, current_user



app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SECRET_KEY'] = 'testing_secret_key'

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

            

        

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup(self):
        with app.app_context():
            response = self.app.post('/signup', data={
                'nome': 'Test User',
                'usuario': 'testuser1',
                'email': 'testuser1@example.com',
                'senha': 'test123',
                'confirmar_senha': 'test123'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            # Verificar se o usuário foi cadastrado corretamente no banco de dados
            user = User.query.filter_by(usuario='testuser1').first()
            self.assertIsNotNone(user)

    def test_login(self):
        with app.app_context():


            # Cadastrar um usuário de teste
            senha = 'testpassword'
            user = User(nome='Kely', usuario='kelyyy', email='kellyaaaa@gmail.com', senhacrip=senha)
            
            db.session.add(user)
            db.session.commit()

            # Teste de login com usuário válido
            response = self.app.post('/', data={
                'email': 'kellyaaaa@gmail.com',
                'senha': senha
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            #verifica se fez o login e entrou no microgram
            self.assertEqual(response.request.path, '/pictures_add')

    def test_logout(self):
        with app.app_context():
            # Cadastrar um usuário de teste
            senha = 'testpassword'
            user = User(nome='Marcelo', usuario='marcelo123', email='marcelo@gmail.com', senhacrip=senha)
            
            db.session.add(user)
            db.session.commit()

            # Teste de login com usuário válido
            response = self.app.post('/', data={
                'email': 'marcelo@gmail.com',
                'senha': senha
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            # Verificar se o usuário está logado corretamente

            # Teste de logout
            response = self.app.get('/logout', follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            # Verificar se o usuário é redirecionado para a página de login após o logout
            self.assertEqual(response.request.path, '/')
            

            
    def test_invalid_user_login(self):
        with app.app_context():
            # Cadastrar um usuário de teste
            senha = 'testpassword'
            user = User(nome='Arnaldo', usuario='arn_morais', email='arnaldo@gmail.com', senhacrip=senha)
            db.session.add(user)
            db.session.commit()

            # Teste de login com email inválido
            response = self.app.post('/', data={
                'email': 'invalidemail@example.com',
                'senha': senha
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            #Não loga e persiste na página de login
            self.assertEqual(response.request.path, '/')


            # Teste de login com senha inválida
            response = self.app.post('/', data={
                'email': 'arnaldo@gmail.com',
                'senha': 'invalidpassword'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            #Não loga e persiste na página de login
            self.assertEqual(response.request.path, '/')
            

    def test_duplicate_username_signup(self):
        with app.app_context():
            # Cadastrar um usuário de teste
            senha = 'testpassword'
            user = User(nome='Kely', usuario='kelyyy', email='kellyaaaa@gmail.com', senha=senha)
            db.session.add(user)
            db.session.commit()

            # Tentar cadastrar um novo usuário com o mesmo nome de usuário
            response = self.app.post('/signup', data={
                'nome': 'Novo Usuário',
                'usuario': 'kelyyy',  # Mesmo nome de usuário do usuário já cadastrado
                'email': 'novousuario@example.com',
                'senha': senha,
                'confirmar_senha': senha
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            #quando cadastra redireciona para a página login, quando não cadatra persiste na página singnup
            self.assertEqual(response.request.path, '/signup')

            

    def test_duplicate_email_signup(self):
        with app.app_context():
            # Cadastrar um usuário de teste
            senha = 'testpassword'
            user = User(nome='Kely', usuario='kelyyy', email='kellyaaaa@gmail.com', senha=senha)
            db.session.add(user)
            db.session.commit()

            # Tentar cadastrar um novo usuário com o mesmo email
            response = self.app.post('/signup', data={
                'nome': 'Novo Usuário',
                'usuario': 'novousuario',
                'email': 'kellyaaaa@gmail.com',  # Mesmo email do usuário já cadastrado
                'senha': senha,
                'confirmar_senha': senha
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            #quando cadastra redireciona para a página login, quando não cadatra persiste na página singnup
            self.assertEqual(response.request.path, '/signup')
            

    def test_user_table_created(self):
        with app.app_context():
            # Verificar se a tabela de usuários está presente no banco de dados
            inspector = db.inspect(db.engine)
            table_names = inspector.get_table_names()
            self.assertIn('user', table_names)
            
            # Verificar se a tabela de usuários tem as colunas esperadas
            table_columns = inspector.get_columns('user')
            expected_columns = ['id', 'nome', 'usuario', 'email', 'senha']
            for column in expected_columns:
                column_names = [col['name'] for col in table_columns]
                self.assertIn(column, column_names)

    def test_signup_user_inserted(self):
        with app.app_context():
            # Dados do usuário para o cadastro
            user_data = {
                'nome': 'Novo Usuário',
                'usuario': 'novo_usuario',
                'email': 'novo_usuario@example.com',
                'senha': 'testpassword',
                'confirmar_senha': 'testpassword'
            }

            # Teste de cadastro de usuário
            response = self.app.post('/signup', data=user_data, follow_redirects=True)

            # Verificar se o cadastro foi bem-sucedido (redirecionamento)
            self.assertEqual(response.status_code, 200)

            # Verificar se o usuário foi inserido corretamente no banco de dados
            inserted_user = User.query.filter_by(usuario='novo_usuario').first()
            self.assertIsNotNone(inserted_user)

            # Verificar as informações do usuário inseridas no banco de dados
            self.assertEqual(inserted_user.nome, 'Novo Usuário')
            self.assertEqual(inserted_user.usuario, 'novo_usuario')
            self.assertEqual(inserted_user.email, 'novo_usuario@example.com')

    def test_list_users(self):
        with app.app_context():
            user1 = User(nome='Kely', usuario='kelyyy', email='kellyaaaa@gmail.com', senha='testpassword')
            db.session.add(user1)
            db.session.commit()

            user2 = User(nome='Kely2', usuario='kelyyy2', email='kellyaaaa2@gmail.com', senha='testpassword2')
            db.session.add(user2)
            db.session.commit()

            user3 = User(nome='Kely3', usuario='kelyyy3', email='kellyaaaa3@gmail.com', senha='testpassword3')
            db.session.add(user3)
            db.session.commit()

            response = self.app.get('/users')
            self.assertEqual(response.status_code, 200)
            for user in User.query.all():
                if user != current_user:
                    self.assertIn(user.nome.encode(), response.data)
    
                

if __name__ == '__main__':
    unittest.main()
