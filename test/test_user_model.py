import unittest
from app import create_app, db
from app.models import User

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        #crea una instancia de la aplicación con la configuración 'testing'
        self.app = create_app('testing')
        #crea un contexto de aplicación para que las extensiones de Flask funcionen
        self.app_context = self.app.app_context()
        self.app_context.push()
        #crea todas las tablas en la base de datos en memoria
        db.create_all()

    def tearDown(self):
        #limpia y elimina la base de datos después de cada prueba
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    #primera prueba: ¿se hashea correctamente la contraseña?
    def test_password_setter(self):
        u = User(username='susan', email='susan@example.com')
        u.set_password('gato')
        self.assertTrue(u.password_hash is not None)
        self.assertNotEqual(u.password_hash, 'gato')

    #segunda prueba: ¿funciona la verificación de contraseñas?
    def test_password_verification(self):
        u = User(username='john', email='john@example.com')
        u.set_password('perro')
        self.assertTrue(u.check_password('perro'))
        self.assertFalse(u.check_password('gato'))

