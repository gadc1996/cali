import functools
from datetime import date
import os

from reportlab.pdfgen import canvas

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from config import config
from cali.lib.db import get_db
from cali.lib.article import get_single_article, Article
from cali.lib.cart import CartItem, ShoppingCart
from cali.lib.sale import Sale
from cali.lib.client import Client

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
    configuration = config.Config()
    if request.method == 'POST':
        pass
    cart = ShoppingCart()
    clients = Client.get_all_clients()
    cart_items = cart.get_all_cart_items()

    return render_template('cart/info.html', cart=cart, cart_items=cart_items, clients=clients, configuration=configuration)

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
    clients = Client.get_all_clients()
    configuration = config.Config()
    sale = Sale(request.form)
    branchId = sale.branchId

    if not sale.client_has_discount():
        g.message = "Cliente Sin Descuento"
        g.messageColor = "danger"
        return render_template('cart/info.html', cart=cart, cart_items=cart_items, clients=clients, configuration=configuration)

    if request.form['Discount'] is not '':
        sale.apply_discount()

    if not cart.there_is_enought_stock(branchId):
        g.message = 'Not enought stock available'
        g.messageColor = 'danger'
        return render_template('cart/info.html', cart=cart, cart_items=cart_items, clients=clients, configuration=configuration)

    if sale.payMethod == 'Cash' and not sale.cash_is_enough(): 
        g.message = 'Not enought cash received'
        g.messageColor = 'danger'
        return render_template('cart/info.html', cart=cart, cart_items=cart_items, clients=clients, configuration=configuration)

    if sale.total == '0':
        g.message = 'Empty Sale'
        g.messageColor = 'danger'
        return render_template('cart/info.html', cart=cart, cart_items=cart_items, clients=clients, configuration=configuration)

    sale.create_sale_ticket(cart_items)
    sale.print_sale_ticket(cart_items)
    db.execute(sale.create_sale(cart_items))
    db.execute(cart.clear_cart())

    for sku, quantity in cart.ticket.items():
        db.execute(cart.update_cartItem_stock(sku, quantity, branchId))

    db.commit()


    return render_template('cart/checkout.html', sale=sale, configuration=configuration)


