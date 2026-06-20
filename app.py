# ============================================================
# LICORERA INTELIGENTE - Aplicación principal Flask
# ============================================================
# Punto de entrada de la aplicación. Configura Flask,
# la base de datos SQLite y registra todos los módulos.
# ============================================================

from flask import Flask, redirect, url_for
from flask_login import LoginManager
from database import db, init_db
from models.user import User
from routes.auth import auth_bp
from routes.inventory import inventory_bp
from routes.sales import sales_bp
from routes.deliveries import deliveries_bp
from routes.dashboard import dashboard_bp
from routes.reports import reports_bp
from routes.store import store_bp
from routes.cashregister import cashregister_bp
import os

# --- Crear instancia de Flask ---
app = Flask(__name__)

# --- Configuración general ---
app.config['SECRET_KEY'] = 'licorera-inteligente-secret-2024'
import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///licorera.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Inicializar SQLAlchemy con la app ---
db.init_app(app)

# --- Configurar Flask-Login ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'          # Redirige si no hay sesión
login_manager.login_message = 'Por favor inicia sesión para continuar.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    """Carga el usuario desde la base de datos por su ID."""
    return User.query.get(int(user_id))

# --- Registrar Blueprints (módulos) ---
app.register_blueprint(auth_bp,       url_prefix='/auth')
app.register_blueprint(inventory_bp,  url_prefix='/inventory')
app.register_blueprint(sales_bp,      url_prefix='/sales')
app.register_blueprint(deliveries_bp, url_prefix='/deliveries')
app.register_blueprint(dashboard_bp,  url_prefix='/')
app.register_blueprint(reports_bp,    url_prefix='/reports')
app.register_blueprint(store_bp, url_prefix='/store')
app.register_blueprint(cashregister_bp, url_prefix='/cashregister')

# --- Ruta raíz: redirige al dashboard ---
@app.route('/')
def index():
    return redirect(url_for('dashboard.index'))

# --- Crear tablas e insertar datos iniciales ---
with app.app_context():
    init_db(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
