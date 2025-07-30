from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Product
from app.forms import ProductForm

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
@login_required
def list_products():
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort', 'name')
    order = request.args.get('order', 'asc')
    
    # Tri des produits
    if sort_by == 'name':
        if order == 'desc':
            products = Product.query.order_by(Product.name.desc())
        else:
            products = Product.query.order_by(Product.name.asc())
    elif sort_by == 'category':
        if order == 'desc':
            products = Product.query.order_by(Product.category.desc())
        else:
            products = Product.query.order_by(Product.category.asc())
    elif sort_by == 'quantity':
        if order == 'desc':
            products = Product.query.order_by(Product.quantity.desc())
        else:
            products = Product.query.order_by(Product.quantity.asc())
    elif sort_by == 'price':
        if order == 'desc':
            products = Product.query.order_by(Product.price.desc())
        else:
            products = Product.query.order_by(Product.price.asc())
    else:
        products = Product.query.order_by(Product.name.asc())
    
    products = products.paginate(page=page, per_page=10, error_out=False)
    
    return render_template('products/list.html', products=products, sort_by=sort_by, order=order)

@products_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            reference=form.reference.data,
            price=form.price.data,
            quantity=form.quantity.data,
            category=form.category.data,
            description=form.description.data
        )
        db.session.add(product)
        db.session.commit()
        flash(f'Produit "{product.name}" ajouté avec succès!', 'success')
        return redirect(url_for('products.list_products'))
    
    return render_template('products/form.html', form=form, title='Ajouter un produit')

@products_bp.route('/<int:id>')
@login_required
def view_product(id):
    product = Product.query.get_or_404(id)
    return render_template('products/view.html', product=product)

@products_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(original_reference=product.reference, obj=product)
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.reference = form.reference.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        product.category = form.category.data
        product.description = form.description.data
        db.session.commit()
        flash(f'Produit "{product.name}" modifié avec succès!', 'success')
        return redirect(url_for('products.view_product', id=product.id))
    
    return render_template('products/form.html', form=form, product=product, title='Modifier le produit')

@products_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    product_name = product.name
    db.session.delete(product)
    db.session.commit()
    flash(f'Produit "{product_name}" supprimé avec succès!', 'success')
    return redirect(url_for('products.list_products'))

@products_bp.route('/low-stock')
@login_required
def low_stock():
    products = Product.query.filter(Product.quantity < 5).order_by(Product.quantity.asc()).all()
    return render_template('products/low_stock.html', products=products)