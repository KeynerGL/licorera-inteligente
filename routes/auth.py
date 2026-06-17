# ============================================================
# RUTAS: Autenticación
# ============================================================
# Maneja login, logout y gestión de usuarios (solo admin).
# ============================================================

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from database import db
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# --- Decorador para rutas solo de Administrador ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Acceso denegado. Solo administradores.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username, is_active=True).first()

        if user and user.check_password(password):
            login_user(user, remember=True)
            flash(f'¡Bienvenido, {user.full_name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Cierra la sesión del usuario actual."""
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/users')
@login_required
@admin_required
def users():
    """Lista todos los usuarios (solo admin)."""
    all_users = User.query.all()
    return render_template('auth/users.html', users=all_users)


@auth_bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    """Agregar nuevo usuario."""
    if request.method == 'POST':
        username  = request.form.get('username', '').strip()
        full_name = request.form.get('full_name', '').strip()
        password  = request.form.get('password', '')
        role      = request.form.get('role', 'empleado')

        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.', 'danger')
        else:
            new_user = User(username=username, full_name=full_name, role=role)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario creado correctamente.', 'success')
            return redirect(url_for('auth.users'))

    return render_template('auth/add_user.html')


@auth_bp.route('/users/toggle/<int:user_id>')
@login_required
@admin_required
def toggle_user(user_id):
    """Activar o desactivar un usuario."""
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('No puedes desactivarte a ti mismo.', 'warning')
    else:
        user.is_active = not user.is_active
        db.session.commit()
        estado = 'activado' if user.is_active else 'desactivado'
        flash(f'Usuario {estado} correctamente.', 'success')
    return redirect(url_for('auth.users'))
