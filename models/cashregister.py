# ============================================================
# MODELO: Caja Diaria
# ============================================================
from database import db
from datetime import datetime

class CashRegister(db.Model):
    __tablename__ = 'cash_registers'

    id             = db.Column(db.Integer, primary_key=True)
    date           = db.Column(db.Date, nullable=False)
    opening_amount = db.Column(db.Float, default=0)   # Efectivo al abrir
    closing_amount = db.Column(db.Float, default=0)   # Efectivo al cerrar
    sales_total    = db.Column(db.Float, default=0)   # Ventas del día
    expected       = db.Column(db.Float, default=0)   # Lo que debería haber
    difference     = db.Column(db.Float, default=0)   # Diferencia
    notes          = db.Column(db.String(300), default='')
    status         = db.Column(db.String(20), default='Abierta')  # Abierta/Cerrada
    user_id        = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='cash_registers')

    def __repr__(self):
        return f'<CashRegister {self.date} - {self.status}>'