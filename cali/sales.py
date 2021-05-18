import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from config import config
from cali.lib.db import get_db
from cali.lib.sale import Sale

blueprint = Blueprint('sales', __name__, url_prefix='/sales')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    configuration = config.Config()
    if request.method == 'POST':
        sales = Sale.get_filtered_sales(request.form)
    else:
        sales = Sale.get_all_sales()

    salesInformation = Sale.get_sales_information(sales)

    if salesInformation['date'] is not '-':
        Sale.create_report(sales, salesInformation)
        Sale.create_txt_report(sales, salesInformation)
    return render_template('sales/search.html', sales=sales, configuration=configuration, salesInformation=salesInformation)

@blueprint.route('/<int:id>/printTicket', methods=('GET',))
def printTicket(id):
    Sale.print_sale_ticket_by_id(id)
    return redirect(url_for('sales.search'))

@blueprint.route('/printreport', methods=('GET',))
def printReport():
    Sale.print_report()
    return redirect(url_for('sales.search'))

