import functools

from flask import (flash, Blueprint, render_template, redirect, request, url_for)

from config import config
from cali.lib.cart import CartItem, ShoppingCart
from cali.lib.sale import Sale
from cali.lib.client import Client
from cali.lib.alert import Alert

blueprint = Blueprint('cart', __name__, url_prefix='/cart')

@blueprint.route('/add?id=<int:id>', methods=('GET',))
def add(id):
    CartItem.add_cart_item(id)
    return redirect(url_for('articles.search'))

@blueprint.route('/info', methods=('GET', 'POST'))
def info():
    configuration = config.Config()
    cart = ShoppingCart()
    clients = Client.get_all_clients()
    cart_items = cart.cart_items
    return render_template('cart/info.html', cart=cart, cart_items=cart_items, clients=clients, configuration=configuration)

@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    CartItem.delete_cart_item(id)
    return redirect(url_for('cart.info'))

@blueprint.route('/checkout', methods=('POST',))
def checkout():
    sale = Sale(request.form)
    configuration = config.Config()
    cart = ShoppingCart()
    cart_items = cart.cart_items
    clients = Client.get_all_clients()
    branchId = sale.branchId
    if request.form['Discount'] is not '':
        sale.apply_discount()

    if sale.is_valid(branchId):
        sale.create_sale(cart_items, branchId)
        cart.update_cart_items_stock(branchId)
        cart.clear_cart()
        sale.save_sale_ticket(cart_items)
        sale.print_sale_ticket(cart_items)
        Alert.raise_success_alert('Sale Created')
        return render_template('cart/checkout.html', sale=sale, configuration=configuration)

    return render_template('cart/info.html', cart=cart, cart_items=cart_items, clients=clients, configuration=configuration)


