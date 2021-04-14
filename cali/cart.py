import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from cali.lib.db import get_db
from cali.lib.article import get_single_article
from cali.lib.cart import CartItem, ShoppingCart
from cali.lib.client import get_all_clients
from cali.lib.sale import Sale

blueprint = Blueprint('cart', __name__, url_prefix='/cart')

@blueprint.route('/add?id=<int:id>', methods=('GET', 'POST'))
def add(id):
    if request.method == 'POST':
        pass

    db = get_db()
    article = get_single_article(id)
    cartItem = CartItem(article)
    db.execute(cartItem.add_cart_item())
    db.commit()
    return redirect(url_for('articles.search'))


@blueprint.route('/info', methods=('GET', 'POST'))
def info():
    if request.method == 'POST':
        pass
    cart = ShoppingCart()
    clients = get_all_clients()
    cart_items = cart.get_all_cart_items()
    return render_template('cart/info.html', cart=cart, cart_items=cart_items, clients=clients)

@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    db = get_db()
    db.execute(CartItem.delete_cart_item(id))
    db.commit()
    return redirect(url_for('cart.info'))

@blueprint.route('/checkout', methods=('POST',))
def checkout():
    cart = ShoppingCart()
    sale = Sale(request.form)
    db = get_db()
    db.execute(sale.create_sale())
    db.execute(cart.clear_cart())
    db.commit()

    return render_template('cart/checkout.html', sale=sale)


