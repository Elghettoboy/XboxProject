# 1. AGREGAMOS 'request' A LOS IMPORTS
from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from ..forms import LoginForm, RegistrationForm
from ..models import User
from .. import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 2. CAMBIAMOS 'main.inicio' POR 'main.dashboard'
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            # Ahora sí funcionará 'request' porque lo importamos arriba
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Error: Usuario o contraseña incorrectos.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        
        # 3. CORREGIMOS EL REGISTRO:
        # - Usamos 'password' en lugar de 'password_hash'
        # - Agregamos el campo 'email' que es obligatorio en tu base de datos
        new_user = User(
            username=form.username.data, 
            email=form.email.data,   # <--- IMPORTANTE: Faltaba esto
            password=hashed_password # <--- IMPORTANTE: Corregido el nombre
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('¡Tu cuenta ha sido creada! Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('auth.login'))