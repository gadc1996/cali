import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from cali.lib.db import get_db
from cali.lib.sale import Sale

blueprint = Blueprint('sales', __name__, url_prefix='/sales')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    if request.method == 'POST':
        #sales = get_filtered_sales(request.form) 
        pass
    else:
        sales = Sale.get_all_sales()

    return render_template('sales/search.html', sales=sales)

@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        db = get_db()
        sale = sale(request.form)

        if sale_exist(sale):
            g.message = 'sale Exists'
            g.messageColor = 'danger'
            return render_template('sales/create.html')
        else:
            g.message = 'sale Created'
            g.messageColor = 'success'
            db.execute(sale.create_sale())
            db.commit()
            return render_template('sales/create.html')

    return render_template('sales/create.html')

@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    db = get_db()
    sale = sale(get_single_sale(id))
    db.execute(sale.delete_sale(id))
    db.commit()

    return redirect(url_for('sales.search'))

@blueprint.route('<int:id>/update', methods=('GET', 'POST'))
def update(id):
    if request.method == 'POST':
        db = get_db()
        sale = sale(request.form)

        if sale_exist(sale):
            g.message = 'sale Exists'
            g.messageColor = 'danger'
            return render_template('sales/update.html', sale=sale)
        else:
            g.message = 'sale Updated'
            g.messageColor = 'success'
            db.execute(sale.update_sale(id))
            db.commit()
            return render_template('sales/update.html', sale=sale)
    else:
        sale = get_single_sale(id)
        return render_template('sales/update.html', sale=sale)
