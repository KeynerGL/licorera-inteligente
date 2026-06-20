# ============================================================
# RUTAS: Caja Diaria
# ============================================================
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.cashregister import CashRegister
from models.sale import Sale
from database import db
from datetime import datetime, date, timedelta
from sqlalchemy import func

cashregister_bp = Blueprint('cashregister', __name__)


@cashregister_bp.route('/')
@login_required
def index():
    """Lista de cajas diarias."""
    registers = CashRegister.query.order_by(CashRegister.date.desc()).limit(30).all()
    today_register = CashRegister.query.filter_by(date=date.today()).first()
    return render_template('cashregister/index.html',
                           registers=registers,
                           today_register=today_register)


@cashregister_bp.route('/open', methods=['GET', 'POST'])
@login_required
def open_register():
    """Abrir caja del día."""
    # Verificar si ya hay una caja abierta hoy
    existing = CashRegister.query.filter_by(date=date.today()).first()
    if existing:
        flash('Ya hay una caja abierta para hoy.', 'warning')
        return redirect(url_for('cashregister.index'))

    if request.method == 'POST':
        try:
            register = CashRegister(
                date           = date.today(),
                opening_amount = float(request.form.get('opening_amount', 0)),
                notes          = request.form.get('notes', ''),
                status         = 'Abierta',
                user_id        = current_user.id
            )
            db.session.add(register)
            db.session.commit()
            flash('✅ Caja abierta correctamente.', 'success')
            return redirect(url_for('cashregister.index'))
        except ValueError:
            flash('Error en los datos ingresados.', 'danger')

    return render_template('cashregister/open.html')


@cashregister_bp.route('/close/<int:register_id>', methods=['GET', 'POST'])
@login_required
def close_register(register_id):
    """Cerrar caja del día."""
    register = CashRegister.query.get_or_404(register_id)

    if register.status == 'Cerrada':
        flash('Esta caja ya está cerrada.', 'warning')
        return redirect(url_for('cashregister.index'))

    # Calcular ventas del día
    dt_start = datetime.combine(register.date, datetime.min.time())
    dt_end   = datetime.combine(register.date, datetime.max.time())
    sales_total = db.session.query(
        func.coalesce(func.sum(Sale.total), 0)
    ).filter(Sale.created_at.between(dt_start, dt_end)).scalar()

    if request.method == 'POST':
        try:
            closing_amount = float(request.form.get('closing_amount', 0))
            expected       = register.opening_amount + sales_total
            difference     = closing_amount - expected

            register.closing_amount = closing_amount
            register.sales_total    = sales_total
            register.expected       = expected
            register.difference     = difference
            register.notes          = request.form.get('notes', register.notes)
            register.status         = 'Cerrada'
            db.session.commit()

            flash(f'✅ Caja cerrada. Diferencia: ${difference:,.0f}', 
                  'success' if difference == 0 else 'warning')
            return redirect(url_for('cashregister.index'))
        except ValueError:
            flash('Error en los datos ingresados.', 'danger')

    return render_template('cashregister/close.html',
                           register=register,
                           sales_total=sales_total)