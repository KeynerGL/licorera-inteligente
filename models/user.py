# ============================================================
# MODELO: Usuario
# ============================================================
# Define la tabla 'users' con autenticación y roles.
# Usa Werkzeug para hashear contraseñas de forma segura.
# ============================================================

from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(50), unique=True, nullable=False)
    full_name  = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role       = db.Column(db.String(20), default='empleado')  # 'admin' o 'empleado'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active  = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        """Hashea y almacena la contraseña."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña ingresada coincide con el hash."""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """Retorna True si el usuario es administrador."""
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'
