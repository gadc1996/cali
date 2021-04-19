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
        filtered_sale = True
    else:
        filtered_sale = False
        sales = Sale.get_all_sales()

    salesInformation = Sale.get_sales_information(sales, filtered_sale)

    return render_template('sales/search.html', sales=sales, configuration=configuration)


