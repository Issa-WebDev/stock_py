from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Product, Sale
from app.forms import SaleForm
from datetime import datetime

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/')
@login_required
def list_sales():
    page = request.args.get('page', 1, type=int)
    sales = Sale.query.order_by(Sale.sale_date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('sales/list.html', sales=sales)

@sales_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_sale():
    form = SaleForm()
    
    if form.validate_on_submit():
        product = Product.query.get(form.product_id.data)
        quantity_sold = form.quantity_sold.data
        
        # Vérifier si il y a assez de stock
        if product.quantity < quantity_sold:
            flash(f'Stock insuffisant! Stock disponible: {product.quantity}', 'danger')
            return render_template('sales/form.html', form=form, title='Enregistrer une vente')
        
        # Créer la vente
        sale = Sale(
            product_id=product.id,
            user_id=current_user.id,
            quantity_sold=quantity_sold,
            unit_price=product.price,
            total_price=product.price * quantity_sold
        )
        
        # Réduire le stock
        product.quantity -= quantity_sold
        
        db.session.add(sale)
        db.session.commit()
        
        flash(f'Vente enregistrée avec succès! {quantity_sold} x {product.name} - Total: {sale.total_price:.2f}€', 'success')
        return redirect(url_for('sales.list_sales'))
    
    return render_template('sales/form.html', form=form, title='Enregistrer une vente')

@sales_bp.route('/<int:id>')
@login_required
def view_sale(id):
    sale = Sale.query.get_or_404(id)
    return render_template('sales/view.html', sale=sale)

@sales_bp.route('/history')
@login_required
def sales_history():
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Sale.query
    
    # Filtrage par dates
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Sale.sale_date >= start_date)
        except ValueError:
            flash('Format de date invalide', 'danger')
    
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Sale.sale_date <= end_date)
        except ValueError:
            flash('Format de date invalide', 'danger')
    
    sales = query.order_by(Sale.sale_date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Statistiques
    total_sales = sum(sale.total_price for sale in query.all())
    total_items_sold = sum(sale.quantity_sold for sale in query.all())
    
    return render_template('sales/history.html', 
                         sales=sales, 
                         total_sales=total_sales,
                         total_items_sold=total_items_sold)