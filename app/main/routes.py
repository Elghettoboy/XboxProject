from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Juego, Reto, Recomendacion, ProgresoReto, Suscripcion

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@main_bp.route("/home")
def home():
    # Si el usuario ya se logueó, lo mandamos directo a su dashboard de Xbox
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route("/dashboard")
@login_required
def dashboard():
    # 1. Obtener información de suscripción
    suscripcion = current_user.suscripcion
    
    # 2. Obtener recomendaciones personalizadas (Join con la tabla Juego)
    recomendaciones = Recomendacion.query.filter_by(user_id=current_user.id).all()
    
    # 3. Obtener retos y el progreso del usuario
    # Hacemos una consulta que nos traiga los retos y si el usuario tiene progreso en ellos
    retos_activos = Reto.query.all()
    
    # Crear un diccionario simple para pasar al template con el estado del reto
    lista_retos = []
    for reto in retos_activos:
        progreso = ProgresoReto.query.filter_by(id_usuario=current_user.id, id_reto=reto.id).first()
        
        datos_reto = {
            'titulo': reto.titulo,
            'descripcion': reto.descripcion,
            'xp': reto.xp_recompensa,
            'objetivo': reto.objetivo_valor,
            'actual': progreso.valor_actual if progreso else 0,
            'completado': progreso.completado if progreso else False,
            'porcentaje': (progreso.valor_actual / reto.objetivo_valor * 100) if progreso else 0
        }
        lista_retos.append(datos_reto)

    return render_template('dashboard.html', 
                           user=current_user,
                           suscripcion=suscripcion,
                           recomendaciones=recomendaciones,
                           retos=lista_retos)