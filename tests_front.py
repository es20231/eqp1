import unittest
from projeto import app, db
from projeto.models import User
from bs4 import BeautifulSoup

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SECRET_KEY'] = 'testing_secret_key'


class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def get_soup(self, url):
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        return BeautifulSoup(response.data, 'html.parser')

    def test_login(self):
        soup = self.get_soup('/')
        self.assertIn(b'<!DOCTYPE html>', soup.encode())
        self.assertIn(b'<title>Login</title>', soup.encode())

    def test_signup(self):
        soup = self.get_soup('/signup')
        self.assertIn(b'<!DOCTYPE html>', soup.encode())
        self.assertIn(b'<title>signup</title>', soup.encode())

    def test_dashboard(self):
        soup = self.get_soup('/dashboard')
        self.assertIn(b'<!DOCTYPE html>', soup.encode())
        self.assertIn(b'<title>Dashboard</title>', soup.encode())

    # def test_pictures_add(self):
    #     with app.app_context():
    #         user = User(nome='Test User', usuario='testuser', email='test@example.com', senha='testpassword')
    #         db.session.add(user)
    #         db.session.commit()

    #         response = self.app.post('/', data={
    #             'email': 'testuser@example.com',
    #             'senha': 'testpassword'
    #         }, follow_redirects=True)
    #         self.assertEqual(response.status_code, 200)
    #         soup = self.get_soup('/pictures_add')
    #         self.assertIn(b'<!DOCTYPE html>', soup.encode())
            
    def test_login_and_redirect_to_pictures_add(self):
        with app.app_context():
            # Criar um usuário de teste
            user = User(nome='Test User', usuario='testuser', email='test@example.com', senhacrip='testpassword')
            db.session.add(user)
            db.session.commit()

            # Fazer a requisição para a página de login com as credenciais corretas
            response = self.app.post('/', data={
                'email': 'test@example.com',
                'senha': 'testpassword'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            self.assertEqual(response.request.path, '/pictures_add')

            #Verificar se o redirecionamento para /pictures_add ocorreu
            self.assertIn(b'<title>Dashboard</title>', response.data)

    def test_login_and_redirect_to_perfil(self):
        with app.app_context():
            # Criar um usuário de teste
            user = User(nome='Test User', usuario='testuser', email='test@example.com', senhacrip='testpassword')
            db.session.add(user)
            db.session.commit()

            # Fazer a requisição para a página de login com as credenciais corretas
            response = self.app.post('/', data={
                'email': 'test@example.com',
                'senha': 'testpassword'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            self.assertEqual(response.request.path, '/pictures_add')
            soup = self.get_soup('/perfil/5')
            self.assertIn(b'<!DOCTYPE html>', soup.encode())

            #Verificar se o redirecionamento para /pictures_add ocorreu
            self.assertIn(b'<title>Dashboard</title>', soup.encode())

    def test_login_and_redirect_to_gallery(self):
        with app.app_context():
            # Criar um usuário de teste
            user = User(nome='Test User', usuario='testuser', email='test@example.com', senhacrip='testpassword')
            db.session.add(user)
            db.session.commit()

            # Fazer a requisição para a página de login com as credenciais corretas
            response = self.app.post('/', data={
                'email': 'test@example.com',
                'senha': 'testpassword'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            self.assertEqual(response.request.path, '/pictures_add')
            soup = self.get_soup('/gallery')
            self.assertIn(b'<!DOCTYPE html>', soup.encode())

            #Verificar se o redirecionamento para /pictures_add ocorreu
            self.assertIn(b'<title>Dashboard</title>', soup.encode())

    def test_users(self):
        soup = self.get_soup('/users')
        self.assertIn(b'<!DOCTYPE html>', soup.encode())
        self.assertIn(b'<title>Dashboard</title>', soup.encode())

if __name__ == '__main__':
    unittest.main()