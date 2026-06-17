# ============================================================
# LICORERA INTELIGENTE - Configuración de Base de Datos
# ============================================================
# Define la instancia de SQLAlchemy y la función init_db
# que crea las tablas y agrega datos de prueba iniciales.
# ============================================================

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

def init_db(app):
    """Crea todas las tablas y agrega datos iniciales si no existen."""
    db.create_all()

    # Importamos aquí para evitar importaciones circulares
    from models.user import User
    from models.product import Product
    from models.sale import Sale, SaleItem
    from models.delivery import Delivery

    # --- Crear usuario Administrador por defecto ---
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            full_name='Administrador',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)

    # --- Crear usuario Empleado por defecto ---
    if not User.query.filter_by(username='empleado').first():
        emp = User(
            username='empleado',
            full_name='Empleado',
            role='empleado'
        )
        emp.set_password('emp123')
        db.session.add(emp)

    # --- Agregar productos de ejemplo ---
    if not Product.query.first():
        products = [
            Product(name='Águila 330ml',        category='Cerveza',     quantity=48, purchase_price=1800,  sale_price=2500,  min_stock=12),
            Product(name='Club Colombia 330ml',  category='Cerveza',     quantity=36, purchase_price=2200,  sale_price=3000,  min_stock=12),
            Product(name='Poker 330ml',          category='Cerveza',     quantity=60, purchase_price=1700,  sale_price=2200,  min_stock=12),
            Product(name='Aguardiente Antioqueño 750ml', category='Aguardiente', quantity=10, purchase_price=22000, sale_price=30000, min_stock=5),
            Product(name='Aguardiente Nectar 750ml',     category='Aguardiente', quantity=8,  purchase_price=20000, sale_price=28000, min_stock=5),
            Product(name='Ron Caldas 750ml',     category='Ron',         quantity=6,  purchase_price=28000, sale_price=38000, min_stock=3),
            Product(name='Ron Medellín 750ml',   category='Ron',         quantity=4,  purchase_price=30000, sale_price=42000, min_stock=3),
            Product(name='Whisky Old Parr 750ml',category='Whisky',      quantity=3,  purchase_price=85000, sale_price=120000,min_stock=2),
            Product(name='Vino Gato Negro Tinto',category='Vino',        quantity=5,  purchase_price=18000, sale_price=26000, min_stock=3),
            Product(name='Maní Tostado 100g',    category='Snacks',      quantity=20, purchase_price=1500,  sale_price=2500,  min_stock=10),
            Product(name='Papas Margarita 70g',  category='Snacks',      quantity=15, purchase_price=2000,  sale_price=3000,  min_stock=10),
            Product(name='Cigarrillos Marlboro',  category='Otros',      quantity=10, purchase_price=12000, sale_price=16000, min_stock=5),
        ]
        for p in products:
            db.session.add(p)

    db.session.commit()
    print("✅ Base de datos inicializada correctamente.")
