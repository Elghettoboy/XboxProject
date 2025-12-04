from app import db
from flask_login import UserMixin
from datetime import datetime

# --- MODELO USUARIO ---
class User(UserMixin, db.Model):
    __tablename__ = 'usuario'  # <--- MINÚSCULAS IMPORTANTE
    
    id = db.Column('id_usuario', db.Integer, primary_key=True)
    username = db.Column('gamertag', db.String(50), unique=True, nullable=False)
    password = db.Column('password_hash', db.String(255), nullable=False)
    email = db.Column('email', db.String(120)) 
    
    # Resto de campos...
    region = db.Column(db.String(50))
    puntos_reward = db.Column(db.Integer, default=0)
    gamerscore = db.Column(db.Integer, default=0)
    
    # Relaciones
    suscripcion = db.relationship('Suscripcion', backref='usuario', uselist=False, lazy=True)
    recomendaciones = db.relationship('Recomendacion', backref='usuario', lazy=True)
    retos_progreso = db.relationship("ProgresoReto", back_populates="usuario")
    
    def __repr__(self):
        return f"User('{self.username}')"

# --- MODELO SUSCRIPCIÓN ---
class Suscripcion(db.Model):
    __tablename__ = 'suscripcion' # <--- MINÚSCULAS
    id = db.Column('id_suscripcion', db.Integer, primary_key=True)
    tipo_plan = db.Column(db.String(20), nullable=False) 
    estado = db.Column('estado', db.String(20), default='Activa')
    fecha_fin = db.Column(db.Date)
    user_id = db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)

# --- MODELO JUEGO ---
class Juego(db.Model):
    __tablename__ = 'juego' # <--- MINÚSCULAS
    id = db.Column('id_juego', db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    desarrollador = db.Column(db.String(100))
    score_metacritic = db.Column(db.Float)
    fecha_lanzamiento = db.Column(db.Date)

# --- MODELO RETO ---
class Reto(db.Model):
    __tablename__ = 'reto'
    id = db.Column('id_reto', db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255)) 
    xp_recompensa = db.Column('puntos_xp', db.Integer) 
    objetivo_valor = db.Column(db.Integer)
    tipo_periodo = db.Column(db.String(20))
    usuarios_progreso = db.relationship("ProgresoReto", back_populates="reto")
    
# --- MODELO RECOMENDACIÓN ---
class Recomendacion(db.Model):
    __tablename__ = 'recomendacion' # <--- MINÚSCULAS
    id = db.Column('id_reco', db.Integer, primary_key=True)
    user_id = db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    juego_id = db.Column('id_juego', db.Integer, db.ForeignKey('juego.id_juego'), nullable=False)
    motivo = db.Column('algoritmo_origen', db.String(50))
    juego = db.relationship('Juego')

# --- PROGRESO RETO ---
class ProgresoReto(db.Model):
    __tablename__ = 'progreso_reto' # <--- MINÚSCULAS
    id = db.Column('id_progreso', db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    id_reto = db.Column(db.Integer, db.ForeignKey('reto.id_reto'))
    valor_actual = db.Column(db.Integer, default=0)
    completado = db.Column(db.Boolean, default=False)
    usuario = db.relationship("User", back_populates="retos_progreso")
    reto = db.relationship("Reto", back_populates="usuarios_progreso")
    
class SesionJuego(db.Model):
    __tablename__ = 'sesion_juego'
    id = db.Column('id_sesion', db.Integer, primary_key=True)
    
    # Claves foráneas (conectan con Usuario y Juego)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    id_juego = db.Column(db.Integer, db.ForeignKey('juego.id_juego'))
    
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    duracion_minutos = db.Column(db.Integer)
    
    # Relaciones para poder decir "sesion.juego.titulo"
    juego = db.relationship('Juego')
    usuario = db.relationship('User', backref='sesiones')
    
# --- MODELO RECOMPENSA ---
class Recompensa(db.Model):
    __tablename__ = 'recompensa'
    id = db.Column('id_recompensa', db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    costo = db.Column('costo_puntos', db.Integer, nullable=False)
    tipo = db.Column(db.String(50)) # 'Digital', 'Fisica', etc.
    
    # Método para formatear el precio bonito (ej: 5,000)
    @property
    def costo_formato(self):
        return "{:,}".format(self.costo)
    
class Notificacion(db.Model):
    __tablename__ = 'notificacion'
    id = db.Column('id_notificacion', db.Integer, primary_key=True)
    user_id = db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id_usuario'))
    mensaje = db.Column(db.Text, nullable=False)
    tipo = db.Column('tipo_trigger', db.String(50)) # 'Logro', 'Sistema', 'Recomendacion'
    estado = db.Column('estado', db.String(20), default='Pendiente')
    fecha = db.Column('fecha_envio', db.DateTime, default=datetime.utcnow)