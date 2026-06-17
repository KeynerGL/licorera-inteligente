# ============================================================
# MODELO: Domicilio
# ============================================================
# Tabla 'deliveries' para gestionar pedidos a domicilio.
# Estado puede ser: Pendiente, En camino, Entregado.
# ============================================================

from database import db
from datetime import datetime

DELIVERY_STATUSES = ['Pendiente', 'En camino', 'Entregado']

class Delivery(db.Model):
    __tablename__ = 'deliveries'

    id           = db.Column(db.Integer, primary_key=True)
    customer_name= db.Column(db.String(100), nullable=False)  # Nombre del cliente
    address      = db.Column(db.String(200), nullable=False)  # Dirección
    phone        = db.Column(db.String(20), nullable=False)   # Teléfono
    notes        = db.Column(db.String(300), default='')      # Notas del pedido
    total        = db.Column(db.Float, default=0)             # Total del pedido
    status       = db.Column(db.String(20), default='Pendiente')  # Estado
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'))  # Quien registró
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación con usuario
    user = db.relationship('User', backref='deliveries')

    @property
    def status_color(self):
        """Retorna clase CSS según el estado del domicilio."""
        colors = {
            'Pendiente': 'warning',
            'En camino': 'info',
            'Entregado': 'success'
        }
        return colors.get(self.status, 'secondary')

    def __repr__(self):
        return f'<Delivery #{self.id} {self.customer_name} - {self.status}>'
