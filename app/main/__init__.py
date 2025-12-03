from flask import Blueprint

#creamos el Blueprint aquí. 
#flask sabrá buscar las plantillas en la carpeta 'templates' del blueprint.
main_bp = Blueprint('main', __name__, template_folder='templates')

#importamos las rutas al final.

from . import routes
