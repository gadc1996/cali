import functools
from datetime import date

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from cali.lib.db import get_db
from cali.lib.article import get_single_article, Article
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
    today = date.today()

    return render_template('cart/info.html', cart=cart, cart_items=cart_items, clients=clients, today=today)

@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    db = get_db()
    db.execute(CartItem.delete_cart_item(id))
    db.commit()
    return redirect(url_for('cart.info'))

@blueprint.route('/checkout', methods=('POST',))
def checkout():
    db = get_db()
    cart = ShoppingCart()
    cart_items = cart.get_all_cart_items()
    sale = Sale(request.form)
    clients = get_all_clients()
    branchId = sale.branchId

    if not cart.there_is_enought_stock(branchId):
        g.message = 'Not enought stock available'
        g.messageColor = 'danger'
        return render_template('cart/info.html', cart=cart, cart_items=cart_items, clients=clients)

    if sale.payMethod=='Cash' and not sale.cash_is_enough(): 
        g.message = 'Not enought cash received'
        g.messageColor = 'danger'
        return render_template('cart/info.html', cart=cart, cart_items=cart_items, clients=clients)

    #for cartItem in cart_items:
    #    flash(cart.update_cartItem_stock(cartItem, branchId))
        #db.execute(cart.update_cartItem_stock(cartItem, branchId))
        #db.commit()
    for sku, quantity in cart.ticket.items():
        db.execute(cart.update_cartItem_stock(sku, quantity, branchId))

    db.execute(sale.create_sale())
    db.execute(cart.clear_cart())
    #db.commit()

    flash(request.form)
    return render_template('cart/checkout.html', sale=sale)


