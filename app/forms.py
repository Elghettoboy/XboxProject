#importamos las clases necesarias de las librerias
from flask_wtf import FlaskForm
# Añadimos EmailField y los validadores Length y Email
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
#importamos el modelo User para poder hacer consultas a la base de datos y validar datos
#usamos '.models' para una importación relativa dentro del paquete 'app'
from .models import User

class LoginForm(FlaskForm):
   
    #campo para el nombre de usuario. Es un campo de texto (StringField).
    #'Nombre de Usuario' es la etiqueta que se mostrará en el HTML.
    #'validators=[DataRequired()]' significa que este campo no puede dejarse vacío.
    username = StringField('Nombre de Usuario', validators=[DataRequired()])

    #campo para la contraseña. Es un campo de contraseña (PasswordField) que oculta el texto.
    password = PasswordField('Contraseña', validators=[DataRequired()])

    #boton para enviar el formulario.
    submit = SubmitField('Iniciar Sesión')


class RegistrationForm(FlaskForm):
    
    #campo para el nombre de usuario, con validadores para que no esté vacío y tenga una longitud adecuada.
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=4, max=25)])

    #campo para el email. Usamos EmailField que ya incluye una validación básica de formato.
    email = EmailField('Correo Electrónico', validators=[DataRequired(), Email(message='Por favor, introduce una dirección de correo válida.')])

    #campo para el nombre.
    name = StringField('Nombre', validators=[DataRequired()])

    #campo para los apellidos.
    surname = StringField('Apellidos', validators=[DataRequired()])

    #campo para el número de teléfono.
    phone_number = StringField('Teléfono', validators=[DataRequired()])
  
    #campo para la contraseña, con validador de longitud mínima.
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])

    #campo para que el usuario repita la contraseña y así confirmarla.
    #el validador 'EqualTo('password')' asegura que el contenido de este campo sea exactamente igual al del campo 'password'.
    confirm_password = PasswordField(
        'Repetir Contraseña', validators=[DataRequired(), EqualTo('password', message='Las contrasenñas deben coincidir.')])

    #boton para enviar el formulario de registro.
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        #se busca en la base de datos si ya existe un usuario con el nombre que se está intentando registrar.
        user = User.query.filter_by(username=username.data).first()
        #si la consulta encuentra un usuario (es decir, 'user' no es None)...
        if user:
            #se lanza un error de validación con un mensaje para el usuario.
            raise ValidationError('Ese nombre de usuario ya está en uso. Por favor, elige otro.')

   
    def validate_email(self, email):
        #se busca en la base de datos si ya existe un usuario con el email que se está intentando registrar.
        user = User.query.filter_by(email=email.data).first()
        #si la consulta encuentra un usuario...
        if user:
            #se lanza un error de validación.
            raise ValidationError('Ese correo electrónico ya está registrado. Por favor, elige otro.')

