import unittest
from app import create_app, db

class MainRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        #el cliente de pruebas nos permite simular peticiones a nuestras rutas
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    #prueba: ¿la ruta raíz '/' redirige a '/login'?
    def test_index_redirects_to_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302) # 302 es el código para redirección
        self.assertIn('/login', response.location)

    #prueba: ¿la página de login carga bien?
    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200) # 200 significa OK
        #verificamos que el texto 'Iniciar Sesión' esté en la página
        self.assertIn(b'Iniciar Sesi\xc3\xb3n', response.data)

