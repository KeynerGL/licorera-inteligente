# ============================================================
# RUTAS: Reportes
# ============================================================
# Reportes diarios, semanales, mensuales y exportación a PDF
# usando WeasyPrint o xhtml2pdf como fallback.
# ============================================================

from flask import Blueprint, render_template, request, make_response, flash, redirect, url_for
from flask_login import login_required
from models.sale import Sale, SaleItem
from models.product import Product
from database import db
from datetime import datetime, date, timedelta
from sqlalchemy import func
import io

reports_bp = Blueprint('reports', __name__)


def get_report_data(date_from, date_to):
    """Obtiene datos de ventas para un rango de fechas."""
    dt_start = datetime.combine(date_from, datetime.min.time())
    dt_end   = datetime.combine(date_to,   datetime.max.time())

    sales = Sale.query.filter(
        Sale.created_at >= dt_start,
        Sale.created_at <= dt_end
    ).order_by(Sale.created_at.desc()).all()

    total_sales  = sum(s.total  for s in sales)
    total_cost   = sum(s.total_cost for s in sales)
    total_profit = sum(s.profit for s in sales)

    # Productos más vendidos en el período
    top_products = db.session.query(
        Product.name,
        Product.category,
        func.sum(SaleItem.quantity).label('qty'),
        func.sum(SaleItem.subtotal).label('revenue')
    ).join(SaleItem, Product.id == SaleItem.product_id
    ).join(Sale, Sale.id == SaleItem.sale_id
    ).filter(Sale.created_at >= dt_start, Sale.created_at <= dt_end
    ).group_by(Product.id
    ).order_by(func.sum(SaleItem.quantity).desc()
    ).limit(10).all()

    # Ventas agrupadas por día
    daily = db.session.query(
        func.date(Sale.created_at).label('day'),
        func.count(Sale.id).label('count'),
        func.sum(Sale.total).label('total'),
        func.sum(Sale.profit).label('profit')
    ).filter(Sale.created_at >= dt_start, Sale.created_at <= dt_end
    ).group_by(func.date(Sale.created_at)
    ).order_by(func.date(Sale.created_at)).all()

    return {
        'sales'        : sales,
        'total_sales'  : total_sales,
        'total_cost'   : total_cost,
        'total_profit' : total_profit,
        'top_products' : top_products,
        'daily'        : daily,
        'date_from'    : date_from,
        'date_to'      : date_to,
        'num_sales'    : len(sales)
    }


@reports_bp.route('/')
@login_required
def index():
    """Página principal de reportes."""
    return render_template('reports/index.html', today=date.today().strftime('%Y-%m-%d'))


@reports_bp.route('/daily')
@login_required
def daily():
    """Reporte del día actual."""
    report_date = request.args.get('date', date.today().strftime('%Y-%m-%d'))
    try:
        d = datetime.strptime(report_date, '%Y-%m-%d').date()
    except ValueError:
        d = date.today()
    data = get_report_data(d, d)
    return render_template('reports/report.html', **data, report_type='Diario',
                           period=d.strftime('%d de %B de %Y'))


@reports_bp.route('/weekly')
@login_required
def weekly():
    """Reporte de la semana actual (lunes a hoy)."""
    today     = date.today()
    monday    = today - timedelta(days=today.weekday())
    data      = get_report_data(monday, today)
    return render_template('reports/report.html', **data, report_type='Semanal',
                           period=f'{monday.strftime("%d/%m/%Y")} - {today.strftime("%d/%m/%Y")}')


@reports_bp.route('/monthly')
@login_required
def monthly():
    """Reporte del mes actual."""
    today     = date.today()
    first_day = date(today.year, today.month, 1)
    data      = get_report_data(first_day, today)
    return render_template('reports/report.html', **data, report_type='Mensual',
                           period=today.strftime('%B %Y'))


@reports_bp.route('/custom', methods=['POST'])
@login_required
def custom():
    """Reporte por rango de fechas personalizado."""
    date_from_str = request.form.get('date_from', '')
    date_to_str   = request.form.get('date_to', '')
    try:
        df = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        dt = datetime.strptime(date_to_str,   '%Y-%m-%d').date()
        if df > dt:
            df, dt = dt, df
    except ValueError:
        flash('Fechas inválidas.', 'danger')
        return redirect(url_for('reports.index'))

    data = get_report_data(df, dt)
    return render_template('reports/report.html', **data, report_type='Personalizado',
                           period=f'{df.strftime("%d/%m/%Y")} - {dt.strftime("%d/%m/%Y")}')


@reports_bp.route('/pdf/<string:report_type>')
@login_required
def export_pdf(report_type):
    """Genera y descarga el reporte en PDF."""
    today = date.today()

    if report_type == 'daily':
        d    = today
        data = get_report_data(d, d)
        period = d.strftime('%d de %B de %Y')
        label  = 'Diario'
    elif report_type == 'weekly':
        monday = today - timedelta(days=today.weekday())
        data   = get_report_data(monday, today)
        period = f'{monday.strftime("%d/%m/%Y")} - {today.strftime("%d/%m/%Y")}'
        label  = 'Semanal'
    else:  # monthly
        first  = date(today.year, today.month, 1)
        data   = get_report_data(first, today)
        period = today.strftime('%B %Y')
        label  = 'Mensual'

    # Renderizar plantilla HTML para PDF
    html_content = render_template('reports/pdf_template.html',
                                   **data, report_type=label, period=period)

    # Intentar con WeasyPrint; si no está instalado, usar xhtml2pdf
    try:
        from weasyprint import HTML
        pdf_bytes = HTML(string=html_content).write_pdf()
    except ImportError:
        try:
            from xhtml2pdf import pisa
            pdf_io = io.BytesIO()
            pisa.CreatePDF(html_content.encode('utf-8'), dest=pdf_io)
            pdf_bytes = pdf_io.getvalue()
        except ImportError:
            flash('Instala WeasyPrint o xhtml2pdf para exportar a PDF. '
                  'Ejecuta: pip install xhtml2pdf', 'warning')
            return redirect(url_for('reports.index'))

    response = make_response(pdf_bytes)
    response.headers['Content-Type']        = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=reporte_{report_type}_{today}.pdf'
    return response
