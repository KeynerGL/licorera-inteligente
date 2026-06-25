# ============================================================
# RUTAS: Inventario
# ============================================================
# CRUD completo de productos con alertas de stock bajo.
# ============================================================

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models.product import Product, CATEGORIES
from database import db
from routes.auth import admin_required

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/')
@login_required
def index():
    """Lista todos los productos activos con filtros."""
    category = request.args.get('category', '')
    search   = request.args.get('search', '')
    low_stock = request.args.get('low_stock', '')

    query = Product.query.filter_by(is_active=True)

    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    if low_stock:
        query = query.filter(Product.quantity <= Product.min_stock)

    products   = query.order_by(Product.category, Product.name).all()
    low_count  = Product.query.filter(
        Product.quantity <= Product.min_stock,
        Product.is_active == True
    ).count()

    return render_template(
        'inventory/index.html',
        products=products,
        categories=CATEGORIES,
        current_category=category,
        search=search,
        low_stock=low_stock,
        low_count=low_count
    )


@inventory_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    """Agregar nuevo producto."""
    if request.method == 'POST':
        try:
            product = Product(
                name           = request.form['name'].strip(),
                category       = request.form['category'],
                quantity       = int(request.form['quantity']),
                purchase_price = float(request.form['purchase_price']),
                sale_price     = float(request.form['sale_price']),
                min_stock      = int(request.form.get('min_stock', 5)),
                image_url      = request.form.get('image_url', '').strip()
            )
            db.session.add(product)
            db.session.commit()
            flash(f'Producto "{product.name}" agregado correctamente.', 'success')
            return redirect(url_for('inventory.index'))
        except (ValueError, KeyError) as e:
            flash('Error en los datos ingresados. Verifica los campos.', 'danger')

    return render_template('inventory/form.html', product=None, categories=CATEGORIES)


@inventory_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(product_id):
    """Editar producto existente."""
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        try:
            product.name           = request.form['name'].strip()
            product.category       = request.form['category']
            product.quantity       = int(request.form['quantity'])
            product.purchase_price = float(request.form['purchase_price'])
            product.sale_price     = float(request.form['sale_price'])
            product.min_stock      = int(request.form.get('min_stock', 5))
            product.image_url      = request.form.get('image_url', '').strip()
            db.session.commit()
            flash(f'Producto "{product.name}" actualizado.', 'success')
            return redirect(url_for('inventory.index'))
        except (ValueError, KeyError):
            flash('Error en los datos ingresados.', 'danger')

    return render_template('inventory/form.html', product=product, categories=CATEGORIES)


@inventory_bp.route('/delete/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete(product_id):
    """Eliminar producto (desactivar en lugar de borrar físicamente)."""
    product = Product.query.get_or_404(product_id)
    product.is_active = False
    db.session.commit()
    flash(f'Producto "{product.name}" eliminado.', 'info')
    return redirect(url_for('inventory.index'))


@inventory_bp.route('/api/products')
@login_required
def api_products():
    """API JSON para obtener productos activos con stock > 0 (usado en ventas)."""
    products = Product.query.filter(
        Product.is_active == True,
        Product.quantity > 0
    ).order_by(Product.name).all()

    return jsonify([{
        'id'         : p.id,
        'name'       : p.name,
        'category'   : p.category,
        'quantity'   : p.quantity,
        'sale_price' : p.sale_price,
        'image_url' : p.image_url or ''
    } for p in products])
