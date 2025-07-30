from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Product, Sale
from app.forms import SearchForm
from sqlalchemy import or_

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Statistiques générales
    total_products = Product.query.count()
    total_stock_value = sum(p.price * p.quantity for p in Product.query.all())
    low_stock_products = Product.query.filter(Product.quantity < 5).count()
    recent_sales = Sale.query.order_by(Sale.sale_date.desc()).limit(5).all()
    
    # Produits en stock faible
    low_stock_items = Product.query.filter(Product.quantity < 5).all()
    
    return render_template('dashboard.html',
                         total_products=total_products,
                         total_stock_value=total_stock_value,
                         low_stock_products=low_stock_products,
                         recent_sales=recent_sales,
                         low_stock_items=low_stock_items)

@main_bp.route('/search')
@login_required
def search():
    form = SearchForm()
    products = []
    
    if request.args.get('search_query') or request.args.get('category_filter'):
        query = Product.query
        
        # Recherche par nom ou référence
        search_query = request.args.get('search_query', '')
        if search_query:
            query = query.filter(
                or_(
                    Product.name.contains(search_query),
                    Product.reference.contains(search_query)
                )
            )
        
        # Filtrage par catégorie
        category_filter = request.args.get('category_filter', '')
        if category_filter:
            query = query.filter(Product.category == category_filter)
        
        products = query.all()
    
    return render_template('search.html', form=form, products=products)