# ============================================================
# RUTAS: Tienda Online para Clientes
# ============================================================
from flask import Blueprint, render_template, request, jsonify
from models.product import Product
from models.delivery import Delivery
from database import db

store_bp = Blueprint('store', __name__)

@store_bp.route('/')
def index():
    """Página principal de la tienda."""
    products = Product.query.filter(
        Product.is_active == True,
        Product.quantity > 0
    ).order_by(Product.category, Product.name).all()
    return render_template('store/index.html', products=products)


from app import limiter

@store_bp.route('/order', methods=['POST'])
@limiter.limit("3 per minute")
def place_order():
    """Registrar pedido del cliente."""
    data = request.get_json()

    if not data or not data.get('items'):
        return jsonify({'error': 'No hay productos en el pedido'}), 400

    items_text = '\n'.join([
        f"- {item['name']} x{item['quantity']} = ${item['subtotal']:,.0f}"
        for item in data['items']
    ])

    notes = f"PEDIDO ONLINE:\n{items_text}\nTotal: ${data['total']:,.0f}"

    delivery = Delivery(
        customer_name = data['customer_name'],
        address       = data['address'],
        phone         = data['phone'],
        notes         = notes,
        total         = data['total'],
        status        = 'Pendiente'
    )
    db.session.add(delivery)
    db.session.commit()

    return jsonify({'success': True, 'delivery_id': delivery.id})