# ============================================================
# MODELO: Venta y Detalle de Venta
# ============================================================
# 'Sale' almacena el encabezado de la venta.
# 'SaleItem' almacena cada producto vendido en esa venta.
# ============================================================

from database import db
from datetime import datetime

class Sale(db.Model):
    __tablename__ = 'sales'

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total        = db.Column(db.Float, default=0)     # Total cobrado al cliente
    total_cost   = db.Column(db.Float, default=0)     # Costo total de la venta
    profit       = db.Column(db.Float, default=0)     # Ganancia = total - total_cost
    notes        = db.Column(db.String(200), default='')
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    user  = db.relationship('User', backref='sales')
    items = db.relationship('SaleItem', backref='sale', lazy=True, cascade='all, delete-orphan')

    def calculate_totals(self):
        """Recalcula totales a partir de los ítems."""
        self.total      = sum(i.subtotal for i in self.items)
        self.total_cost = sum(i.quantity * i.purchase_price for i in self.items)
        self.profit     = self.total - self.total_cost

    def __repr__(self):
        return f'<Sale #{self.id} Total:{self.total}>'


class SaleItem(db.Model):
    __tablename__ = 'sale_items'

    id             = db.Column(db.Integer, primary_key=True)
    sale_id        = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    product_id     = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity       = db.Column(db.Integer, nullable=False)
    unit_price     = db.Column(db.Float, nullable=False)     # Precio de venta al momento
    purchase_price = db.Column(db.Float, nullable=False)     # Precio de compra al momento
    subtotal       = db.Column(db.Float, nullable=False)     # quantity * unit_price

    def __repr__(self):
        return f'<SaleItem product:{self.product_id} qty:{self.quantity}>'
