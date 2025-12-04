from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Juego, Reto, Recomendacion, ProgresoReto, Suscripcion, SesionJuego, Recompensa,Notificacion, db
from app.forms import SessionForm
from app.forms import SessionForm, SubscriptionForm
from sqlalchemy import func


main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@main_bp.route("/home")
def home():
    # Si el usuario ya se logueó, lo mandamos directo a su dashboard de Xbox
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route("/registrar_partida", methods=['GET', 'POST'])
@login_required
def registrar_partida():
    form = SessionForm()

    # Llenamos el desplegable con los juegos que tienes en la base de datos
    # (El valor será el ID, y la etiqueta será el Título)
    form.juego_id.choices = [(j.id, j.titulo) for j in Juego.query.all()]

    if form.validate_on_submit():
        # Creamos la nueva sesión
        nueva_sesion = SesionJuego(
            id_usuario=current_user.id,
            id_juego=form.juego_id.data,
            duracion_minutos=form.duracion.data
        )
        # Guardamos en la base de datos
        db.session.add(nueva_sesion)
        db.session.commit()

        # Sumamos puntos al usuario (Gamification extra)
        current_user.gamerscore += 10 
        db.session.commit()

        flash('¡Partida registrada! Has ganado +10 G', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('registrar_partida.html', form=form)

@main_bp.route("/suscripcion", methods=['GET', 'POST'])
@login_required
def suscripcion():
    form = SubscriptionForm()
    mi_sub = current_user.suscripcion

    # Si enviamos el formulario (UPDATE o CREATE)
    if form.validate_on_submit():
        if mi_sub:
            # UPDATE: Ya existe, solo cambiamos el plan
            mi_sub.tipo_plan = form.tipo_plan.data
            mi_sub.estado = 'Activa'
            flash(f'¡Plan actualizado a {form.tipo_plan.data}!', 'success')
        else:
            # CREATE: No existe, creamos una nueva
            nueva_sub = Suscripcion(
                user_id=current_user.id,
                tipo_plan=form.tipo_plan.data,
                estado='Activa'
            )
            db.session.add(nueva_sub)
            flash(f'¡Bienvenido a Game Pass {form.tipo_plan.data}!', 'success')
        
        db.session.commit()
        return redirect(url_for('main.dashboard'))

    return render_template('suscripcion.html', form=form, sub=mi_sub)

# --- RUTA 2: CANCELAR SUSCRIPCIÓN (DELETE LÓGICO) ---
@main_bp.route("/cancelar_suscripcion")
@login_required
def cancelar_suscripcion():
    mi_sub = current_user.suscripcion
    if mi_sub:
        # No borramos el registro, solo cambiamos el estado (Soft Delete)
        mi_sub.estado = 'Cancelada'
        db.session.commit()
        flash('Tu suscripción ha sido cancelada.', 'warning')
    return redirect(url_for('main.dashboard'))


# --- TIENDA DE REWARDS ---
@main_bp.route("/rewards")
@login_required
def rewards():
    # READ: Traemos todos los premios
    premios = Recompensa.query.all()
    return render_template('rewards.html', premios=premios, user=current_user)

# --- CANJEAR PREMIO (LÓGICA) ---
@main_bp.route("/canjear/<int:id_premio>")
@login_required
def canjear(id_premio):
    premio = Recompensa.query.get_or_404(id_premio)
    
    # 1. Validar si le alcanzan los puntos
    if current_user.puntos_reward >= premio.costo:
        # UPDATE: Restar puntos
        current_user.puntos_reward -= premio.costo
        db.session.commit()
        
        flash(f'¡Canje exitoso! Disfruta tu {premio.nombre}. Se envió el código a tu correo.', 'success')
    else:
        faltante = premio.costo - current_user.puntos_reward
        flash(f'No tienes puntos suficientes. Te faltan {faltante} pts.', 'danger')
        
    return redirect(url_for('main.rewards'))



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

@main_bp.route("/perfil")
@login_required
def perfil():
    # 1. Traer todas las sesiones de este usuario ordenadas por fecha (más reciente primero)
    historial = SesionJuego.query.filter_by(id_usuario=current_user.id).order_by(SesionJuego.fecha_inicio.desc()).all()
    
    # 2. Calcular total de minutos jugados
    total_minutos = db.session.query(func.sum(SesionJuego.duracion_minutos)).filter_by(id_usuario=current_user.id).scalar() or 0
    total_horas = round(total_minutos / 60, 1)

    return render_template('perfil.html', user=current_user, historial=historial, horas=total_horas)

@main_bp.context_processor
def inject_notifications():
    if current_user.is_authenticated:
        # Contamos cuántas notificaciones tiene en estado 'Pendiente'
        pendientes = Notificacion.query.filter_by(user_id=current_user.id, estado='Pendiente').count()
        return dict(num_notificaciones=pendientes)
    return dict(num_notificaciones=0)

@main_bp.route("/notificaciones")
@login_required
def ver_notificaciones():
    # 1. Traer todas las notificaciones (las más nuevas primero)
    mis_notifs = Notificacion.query.filter_by(user_id=current_user.id).order_by(Notificacion.fecha.desc()).all()
    
    # 2. Marcar todas como 'Vista' al abrir la página (UPDATE masivo)
    for n in mis_notifs:
        if n.estado == 'Pendiente':
            n.estado = 'Vista'
    db.session.commit()
    
    return render_template('notificaciones.html', notificaciones=mis_notifs)