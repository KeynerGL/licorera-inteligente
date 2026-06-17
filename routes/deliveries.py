# ============================================================
# RUTAS: Domicilios
# ============================================================
# Gestión de pedidos a domicilio con cambio de estado.
# ============================================================

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models.delivery import Delivery, DELIVERY_STATUSES
from database import db
from datetime import datetime, date, timedelta

deliveries_bp = Blueprint('deliveries', __name__)


@deliveries_bp.route('/')
@login_required
def index():
    """Lista de domicilios con filtro por estado."""
    status_filter = request.args.get('status', '')
    date_filter   = request.args.get('date', date.today().strftime('%Y-%m-%d'))

    try:
        filter_date = datetime.strptime(date_filter, '%Y-%m-%d')
        next_day    = filter_date + timedelta(days=1)
    except ValueError:
        filter_date = datetime.combine(date.today(), datetime.min.time())
        next_day    = filter_date + timedelta(days=1)

    query = Delivery.query.filter(
        Delivery.created_at >= filter_date,
        Delivery.created_at <  next_day
    )

    if status_filter:
        query = query.filter_by(status=status_filter)

    deliveries = query.order_by(Delivery.created_at.desc()).all()

    # Contadores por estado (todos los días)
    pending   = Delivery.query.filter_by(status='Pendiente').count()
    en_camino = Delivery.query.filter_by(status='En camino').count()

    return render_template(
        'deliveries/index.html',
        deliveries=deliveries,
        statuses=DELIVERY_STATUSES,
        status_filter=status_filter,
        date_filter=date_filter,
        pending=pending,
        en_camino=en_camino
    )


@deliveries_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Registrar nuevo domicilio."""
    if request.method == 'POST':
        try:
            delivery = Delivery(
                customer_name = request.form['customer_name'].strip(),
                address       = request.form['address'].strip(),
                phone         = request.form['phone'].strip(),
                notes         = request.form.get('notes', '').strip(),
                total         = float(request.form.get('total', 0)),
                user_id       = current_user.id
            )
            db.session.add(delivery)
            db.session.commit()
            flash(f'Domicilio para "{delivery.customer_name}" registrado.', 'success')
            return redirect(url_for('deliveries.index'))
        except (ValueError, KeyError):
            flash('Error al registrar el domicilio. Verifica los datos.', 'danger')

    return render_template('deliveries/form.html', delivery=None, statuses=DELIVERY_STATUSES)


@deliveries_bp.route('/edit/<int:delivery_id>', methods=['GET', 'POST'])
@login_required
def edit(delivery_id):
    """Editar un domicilio existente."""
    delivery = Delivery.query.get_or_404(delivery_id)

    if request.method == 'POST':
        try:
            delivery.customer_name = request.form['customer_name'].strip()
            delivery.address       = request.form['address'].strip()
            delivery.phone         = request.form['phone'].strip()
            delivery.notes         = request.form.get('notes', '').strip()
            delivery.total         = float(request.form.get('total', 0))
            delivery.status        = request.form.get('status', delivery.status)
            db.session.commit()
            flash('Domicilio actualizado correctamente.', 'success')
            return redirect(url_for('deliveries.index'))
        except (ValueError, KeyError):
            flash('Error al actualizar el domicilio.', 'danger')

    return render_template('deliveries/form.html', delivery=delivery, statuses=DELIVERY_STATUSES)


@deliveries_bp.route('/status/<int:delivery_id>', methods=['POST'])
@login_required
def update_status(delivery_id):
    """Actualizar el estado de un domicilio vía AJAX."""
    delivery   = Delivery.query.get_or_404(delivery_id)
    new_status = request.form.get('status')

    if new_status in DELIVERY_STATUSES:
        delivery.status = new_status
        db.session.commit()
        return jsonify({'success': True, 'status': new_status})

    return jsonify({'error': 'Estado inválido.'}), 400


@deliveries_bp.route('/delete/<int:delivery_id>', methods=['POST'])
@login_required
def delete(delivery_id):
    """Eliminar un domicilio."""
    delivery = Delivery.query.get_or_404(delivery_id)
    db.session.delete(delivery)
    db.session.commit()
    flash('Domicilio eliminado.', 'info')
    return redirect(url_for('deliveries.index'))
