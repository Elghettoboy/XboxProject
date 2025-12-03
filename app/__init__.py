
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config #importamos la configuración

#inicializamos las extensiones
db = SQLAlchemy()
login_manager = LoginManager()

#movemos la configuración de login_manager aquí para que sea más limpio
login_manager.login_view = 'auth.login'
login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."

def create_app():
    
    app = Flask(__name__)

    # aqui importamos lo que tenemos en el archivo .env
    #leemos la variable FLASK_ENV del archivo .env (o del sistema)
    # y cargamos la configuración correspondiente desde nuestro archivo config.py
    config_name = os.getenv('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])

    #inicializamos las extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        
        from .models import User
        return User.query.get(int(user_id))

    
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from .main.routes import main_bp
    app.register_blueprint(main_bp)


    #la condición se asegura de que esto solo se ejecute en producción
    if not app.debug and not app.testing:
        #crea la carpeta 'logs' si no existe
        if not os.path.exists('logs'):
            os.mkdir('logs')
            
        #configura el manejador de archivos que rota los logs
        file_handler = RotatingFileHandler('logs/mi_proyecto_flask.log', maxBytes=10240,
                                           backupCount=10)
        
        #define el formato de cada línea de log
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        
        #establece el nivel de registro (INFO, WARNING, ERROR, etc.)
        file_handler.setLevel(logging.INFO)
        
        #añade el manejador al logger de la aplicación
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('MIPROYECTOFLASK startup')
    
    return app
