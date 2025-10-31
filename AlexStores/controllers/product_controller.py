from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.product import Product
from forms import ProductForm # NOVO

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/')
@login_required
def list_products():
    products = Product.query.filter_by(user_id=current_user.id).all()
    return render_template('products/list.html', products=products)

@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm() # NOVO
    if form.validate_on_submit(): # NOVO: Valida no envio
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            user_id=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        flash('Acessório adicionado')
        return redirect(url_for('product_bp.list_products'))
    # Se GET ou validação falhar, renderiza o template com o formulário (e erros)
    return render_template('products/add.html', form=form) # NOVO: Passa o form

@product_bp.route('/edit/<int:id>', methods=['GET', 'POST']) # NOVO: Rota de edição
@login_required
def edit_product(id):
    product = Product.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    # Preenche o formulário com os dados do produto para GET. Para POST, carrega os dados do request.
    form = ProductForm(obj=product) 

    if form.validate_on_submit():
        # Atualiza o objeto com dados validados
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        db.session.commit()
        flash('Acessório atualizado com sucesso!')
        return redirect(url_for('product_bp.list_products'))
    
    return render_template('products/edit.html', form=form, product=product) # NOVO: Passa o form e o produto

@product_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    if product.user_id != current_user.id:
        flash('Acesso negado')
        return redirect(url_for('product_bp.list_products'))
    db.session.delete(product)
    db.session.commit()
    flash('Acessório excluído')
    return redirect(url_for('product_bp.list_products'))
