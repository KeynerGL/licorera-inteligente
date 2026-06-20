# ============================================================
# RUTAS: Ventas
# ============================================================
# Registro de ventas, descuento automático de inventario,
# cálculo de ganancias e historial.
# ============================================================

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models.sale import Sale, SaleItem
from models.product import Product
from database import db
from utils.whatsapp import send_low_stock_alert
from models.product import Product
from datetime import datetime, date, timedelta
import json

sales_bp = Blueprint('sales', __name__)


@sales_bp.route('/')
@login_required
def index():
    """Historial de ventas con filtro por fecha."""
    date_from = request.args.get('date_from', date.today().strftime('%Y-%m-%d'))
    date_to   = request.args.get('date_to',   date.today().strftime('%Y-%m-%d'))

    try:
        dt_from = datetime.strptime(date_from, '%Y-%m-%d')
        dt_to   = datetime.strptime(date_to,   '%Y-%m-%d') + timedelta(days=1)
    except ValueError:
        dt_from = datetime.combine(date.today(), datetime.min.time())
        dt_to   = dt_from + timedelta(days=1)

    sales = Sale.query.filter(
        Sale.created_at >= dt_from,
        Sale.created_at <  dt_to
    ).order_by(Sale.created_at.desc()).all()

    total_ventas  = sum(s.total  for s in sales)
    total_ganacia = sum(s.profit for s in sales)

    return render_template(
        'sales/index.html',
        sales=sales,
        date_from=date_from,
        date_to=date_to,
        total_ventas=total_ventas,
        total_ganacia=total_ganacia
    )


@sales_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    """Registrar nueva venta."""
    if request.method == 'POST':
        data = request.get_json()

        if not data or not data.get('items'):
            return jsonify({'error': 'No hay productos en la venta.'}), 400

        # Crear encabezado de venta
        sale = Sale(user_id=current_user.id, notes=data.get('notes', ''))
        db.session.add(sale)
        db.session.flush()  # Para obtener sale.id antes del commit

        errors = []

        for item_data in data['items']:
            product = Product.query.get(item_data['product_id'])

            if not product or not product.is_active:
                errors.append(f'Producto ID {item_data["product_id"]} no encontrado.')
                continue

            qty = int(item_data['quantity'])

            if qty > product.quantity:
                errors.append(f'Stock insuficiente para "{product.name}" (disponible: {product.quantity}).')
                continue

            # Crear ítem de venta
            sale_item = SaleItem(
                sale_id        = sale.id,
                product_id     = product.id,
                quantity       = qty,
                unit_price     = product.sale_price,
                purchase_price = product.purchase_price,
                subtotal       = qty * product.sale_price
            )
            db.session.add(sale_item)

            # Descontar del inventario
            product.quantity -= qty

        if errors:
            db.session.rollback()
            return jsonify({'error': '. '.join(errors)}), 400

        # Calcular totales y guardar
        db.session.flush()
        sale.calculate_totals()
        db.session.commit()
        # Verificar stock bajo y enviar alerta WhatsApp
        low_stock = Product.query.filter(
            Product.quantity <= Product.min_stock,
            Product.is_active == True
        ).all()
        if low_stock:
            send_low_stock_alert(low_stock)
        return jsonify({
            'success': True,
            'sale_id': sale.id,
            'total'  : sale.total,
            'profit' : sale.profit
        })

    return render_template('sales/new.html')


@sales_bp.route('/detail/<int:sale_id>')
@login_required
def detail(sale_id):
    """Detalle de una venta específica."""
    sale = Sale.query.get_or_404(sale_id)
    return render_template('sales/detail.html', sale=sale)


@sales_bp.route('/delete/<int:sale_id>', methods=['POST'])
@login_required
def delete(sale_id):
    """Anular una venta y restaurar el inventario (solo admin)."""
    if not current_user.is_admin():
        flash('Solo administradores pueden anular ventas.', 'danger')
        return redirect(url_for('sales.index'))

    sale = Sale.query.get_or_404(sale_id)

    # Restaurar inventario por cada ítem
    for item in sale.items:
        product = Product.query.get(item.product_id)
        if product:
            product.quantity += item.quantity

    db.session.delete(sale)
    db.session.commit()
    flash(f'Venta #{sale_id} anulada y stock restaurado.', 'info')
    return redirect(url_for('sales.index'))
