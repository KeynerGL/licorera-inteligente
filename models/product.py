# ============================================================
# MODELO: Producto (Inventario)
# ============================================================
# Tabla 'products' con categorías, precios y alertas de stock.
# ============================================================

from database import db
from datetime import datetime

# Categorías válidas para la licorera
CATEGORIES = ['Cerveza', 'Aguardiente', 'Ron', 'Whisky', 'Vino', 'Snacks', 'Otros']

class Product(db.Model):
    __tablename__ = 'products'

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(100), nullable=False)
    category       = db.Column(db.String(50), nullable=False)
    quantity       = db.Column(db.Integer, default=0)        # Stock actual
    purchase_price = db.Column(db.Float, nullable=False)     # Precio de compra
    sale_price     = db.Column(db.Float, nullable=False)     # Precio de venta
    min_stock      = db.Column(db.Integer, default=5)        # Stock mínimo para alerta
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at     = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    image_url      = db.Column(db.String(500), default='')
    is_active      = db.Column(db.Boolean, default=True)

    # Relación con ítems de venta
    sale_items = db.relationship('SaleItem', backref='product', lazy=True)

    @property
    def profit_margin(self):
        """Calcula el margen de ganancia por unidad."""
        return self.sale_price - self.purchase_price

    @property
    def profit_percent(self):
        """Calcula el % de ganancia sobre el precio de compra."""
        if self.purchase_price > 0:
            return round((self.profit_margin / self.purchase_price) * 100, 1)
        return 0

    @property
    def is_low_stock(self):
        """Retorna True si el stock está por debajo del mínimo."""
        return self.quantity <= self.min_stock

    def __repr__(self):
        return f'<Product {self.name} - Stock:{self.quantity}>'
