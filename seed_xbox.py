from app import create_app, db
from app.models import User, Juego, Reto, Suscripcion, Recomendacion, ProgresoReto
from werkzeug.security import generate_password_hash

# Inicializar la app
app = create_app()

with app.app_context():
    print("1. Eliminando base de datos antigua...")
    db.drop_all()
    
    print("2. Creando nuevas tablas de Xbox...")
    db.create_all()

    print("3. Insertando datos de prueba...")

    # Crear Usuario
    hashed_pw = generate_password_hash('123456')
    user = User(
        username='GhettoBoy_MX',
        email='ghettoboy@xbox.com',
        password=hashed_pw,
        region='Mexico',
        gamerscore=15420,
        puntos_reward=5000,
        name='Alessandro',
        surname='Sanchez',
        is_admin=True
    )
    db.session.add(user)
    db.session.commit()

    # Crear Suscripción
    sub = Suscripcion(tipo_plan='Ultimate', user_id=user.id)
    db.session.add(sub)

    # Crear Juegos
    juegos = [
        Juego(titulo='Halo Infinite', genero='Shooter', desarrollador='343 Industries', score_metacritic=8.7),
        Juego(titulo='Forza Horizon 5', genero='Carreras', desarrollador='Playground Games', score_metacritic=9.2),
        Juego(titulo='Starfield', genero='RPG', desarrollador='Bethesda', score_metacritic=8.3),
        Juego(titulo='Hi-Fi Rush', genero='Acción', desarrollador='Tango Gameworks', score_metacritic=8.9)
    ]
    db.session.add_all(juegos)
    db.session.commit()

    # Crear Recomendación (Juego 2 = Forza)
    juego_forza = Juego.query.filter_by(titulo='Forza Horizon 5').first()
    rec1 = Recomendacion(user_id=user.id, juego_id=juego_forza.id, motivo="Porque jugaste Forza Motorsport")
    db.session.add(rec1)

    # Crear Retos
    r1 = Reto(titulo='Tirador de Primera', descripcion='50 bajas en multijugador', xp_recompensa=250, objetivo_valor=50, tipo_periodo='Semanal')
    r2 = Reto(titulo='Explorador', descripcion='Juega 3 RPGs diferentes', xp_recompensa=1000, objetivo_valor=3, tipo_periodo='Mensual')
    db.session.add_all([r1, r2])
    db.session.commit()

    # Crear Progreso (Usuario lleva 12 de 50 en el reto 1)
    prog = ProgresoReto(id_usuario=user.id, id_reto=r1.id, valor_actual=12, completado=False)
    db.session.add(prog)

    db.session.commit()
    print("--- ¡LISTO! Base de datos reiniciada y cargada ---")