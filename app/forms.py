from flask_wtf import FlaskForm
# Importamos SOLO lo que sabemos que funciona (quitamos EmailField)
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import User

class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=2, max=20)])
    
    # --- CAMBIO AQUÍ ---
    # Usamos StringField con el validador de Email. Esto hace lo mismo pero no falla.
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ese nombre de usuario ya está en uso. Por favor elige otro.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ese email ya está registrado. Por favor inicia sesión.')

class SessionForm(FlaskForm):
    juego_id = SelectField('Selecciona el Juego', coerce=int)
    duracion = IntegerField('Minutos jugados', validators=[DataRequired()])
    submit = SubmitField('Registrar Partida')

class SubscriptionForm(FlaskForm):
    tipo_plan = SelectField('Elige tu Plan', choices=[
        ('Ultimate', 'Xbox Game Pass Ultimate ($229 MXN)'),
        ('PC', 'PC Game Pass ($149 MXN)'),
        ('Core', 'Xbox Game Pass Core ($169 MXN)')
    ])
    submit = SubmitField('Actualizar Suscripción')