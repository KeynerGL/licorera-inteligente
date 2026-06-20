# ============================================================
# RUTAS: Dashboard e Inteligencia de Negocio
# ============================================================
# Muestra métricas del día, mes y recomendaciones automáticas.
# ============================================================

from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models.sale import Sale, SaleItem
from models.product import Product
from models.delivery import Delivery
from database import db
from datetime import datetime, date, timedelta
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)


def get_sales_today():
    """Total de ventas del día actual."""
    today     = date.today()
    dt_start  = datetime.combine(today, datetime.min.time())
    dt_end    = datetime.combine(today, datetime.max.time())
    result    = db.session.query(
        func.coalesce(func.sum(Sale.total), 0),
        func.coalesce(func.sum(Sale.profit), 0),
        func.count(Sale.id)
    ).filter(Sale.created_at.between(dt_start, dt_end)).first()
    return {'total': result[0], 'profit': result[1], 'count': result[2]}


def get_sales_month():
    """Total de ventas del mes actual."""
    today    = date.today()
    dt_start = datetime(today.year, today.month, 1)
    result   = db.session.query(
        func.coalesce(func.sum(Sale.total), 0),
        func.coalesce(func.sum(Sale.profit), 0),
        func.count(Sale.id)
    ).filter(Sale.created_at >= dt_start).first()
    return {'total': result[0], 'profit': result[1], 'count': result[2]}


def get_top_products(limit=5):
    """Productos más vendidos (por cantidad de unidades)."""
    results = db.session.query(
        Product.name,
        Product.category,
        func.sum(SaleItem.quantity).label('total_qty'),
        func.sum(SaleItem.subtotal).label('total_revenue')
    ).join(SaleItem, Product.id == SaleItem.product_id
    ).group_by(Product.id
    ).order_by(func.sum(SaleItem.quantity).desc()
    ).limit(limit).all()

    return [{'name': r.name, 'category': r.category,
             'qty': int(r.total_qty), 'revenue': float(r.total_revenue)} for r in results]


def get_low_stock_products():
    """Productos con stock bajo."""
    products = Product.query.filter(
        Product.quantity <= Product.min_stock,
        Product.is_active == True
    ).order_by(Product.quantity).all()
    return products


def get_sales_by_day_of_week():
    """Ventas agrupadas por día de la semana (últimas 4 semanas)."""
    four_weeks_ago = datetime.now() - timedelta(weeks=4)
    results = db.session.query(
        func.extract('dow', Sale.created_at).label('dow'),
        func.coalesce(func.sum(Sale.total), 0).label('total')
    ).filter(Sale.created_at >= four_weeks_ago
    ).group_by(func.extract('dow', Sale.created_at)
    ).all()

    days_map  = {0:'Dom', 1:'Lun', 2:'Mar', 3:'Mié', 4:'Jue', 5:'Vie', 6:'Sáb'}
    day_totals = {d: 0 for d in days_map.values()}
    for r in results:
        dow = int(r.dow) if r.dow is not None else 0
        day_totals[days_map.get(dow, '?')] = float(r.total)
    return day_totals

def get_sales_last_7_days():
    """Ventas de los últimos 7 días para gráfica."""
    data = []
    for i in range(6, -1, -1):
        day      = date.today() - timedelta(days=i)
        dt_start = datetime.combine(day, datetime.min.time())
        dt_end   = datetime.combine(day, datetime.max.time())
        total    = db.session.query(
            func.coalesce(func.sum(Sale.total), 0)
        ).filter(Sale.created_at.between(dt_start, dt_end)).scalar()
        data.append({'date': day.strftime('%d/%m'), 'total': float(total)})
    return data


@dashboard_bp.route('/dashboard')
@login_required
def index():
    """Dashboard principal con todas las métricas."""
    today_stats   = get_sales_today()
    month_stats   = get_sales_month()
    top_products  = get_top_products(5)
    low_stock     = get_low_stock_products()
    day_of_week   = get_sales_by_day_of_week()
    last_7_days   = get_sales_last_7_days()
    pending_deliveries = Delivery.query.filter_by(status='Pendiente').count()
    en_camino_deliveries = Delivery.query.filter_by(status='En camino').count()

    # Mejor día de ventas
    best_day = max(day_of_week, key=day_of_week.get) if day_of_week else 'N/A'

    # Recomendaciones de inteligencia de negocio
    recommendations = []
    if low_stock:
        recommendations.append({
            'type': 'warning',
            'icon': '📦',
            'msg' : f'{len(low_stock)} producto(s) con stock bajo. Revisar: {", ".join([p.name for p in low_stock[:3]])}.'
        })
    if top_products:
        recommendations.append({
            'type': 'info',
            'icon': '🏆',
            'msg' : f'Producto estrella: "{top_products[0]["name"]}" es el más vendido. Asegúrate de tener suficiente stock.'
        })
    if best_day != 'N/A':
        recommendations.append({
            'type': 'success',
            'icon': '📅',
            'msg' : f'El día {best_day} es cuando más ventas registras. Prepárate con inventario extra ese día.'
        })
    if pending_deliveries > 0:
        recommendations.append({
            'type': 'danger',
            'icon': '🛵',
            'msg' : f'Tienes {pending_deliveries} domicilio(s) pendiente(s) por despachar.'
        })

    return render_template('dashboard/index.html',
        today_stats   = today_stats,
        month_stats   = month_stats,
        top_products  = top_products,
        low_stock     = low_stock,
        day_of_week   = day_of_week,
        last_7_days   = last_7_days,
        best_day      = best_day,
        recommendations = recommendations,
        pending_deliveries = pending_deliveries,
        en_camino_deliveries = en_camino_deliveries
    )


@dashboard_bp.route('/api/chart-data')
@login_required
def chart_data():
    """API para refrescar datos de gráficas."""
    return jsonify({
        'last_7_days' : get_sales_last_7_days(),
        'top_products': get_top_products(5),
        'day_of_week' : get_sales_by_day_of_week()
    })
