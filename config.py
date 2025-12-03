import os
from dotenv import load_dotenv

#encuentra la ruta base del proyecto para que .env se cargue correctamente
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    #generamos una clave secreta para proteger formularios y sesiones
    #la obtenemos de una variable de entorno para no escribirla en el código
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-por-defecto'
    
    #desactivamos la función de SQLAlchemy que no necesitamos y que consume recursos
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #define el nivel mínimo de registro que queremos ver
    LOG_LEVEL = 'INFO'
    
    # Añadimos LOG_TO_STDOUT para la configuración de logs
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

class DevelopmentConfig(Config):
    DEBUG = True
    # Estructura: postgresql://usuario:contraseña@servidor/nombre_db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgresql://admin:123456@localhost/xboxdb'

class ProductionConfig(Config):
    DEBUG = False
    #para producción, es crucial que la URL de la BD venga de una variable de entorno
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    #habilita el modo de pruebas de Flask
    TESTING = True
    #usaremos una base de datos SQLite en memoria para que las pruebas sean rápidas y aisladas
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    #desactivamos la protección CSRF en los formularios, ya que en las pruebas no la necesitamos
    WTF_CSRF_ENABLED = False


#un diccionario para acceder fácilmente a las clases de configuración
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig, # Añadimos la nueva configuración de pruebas
    'default': DevelopmentConfig
}

