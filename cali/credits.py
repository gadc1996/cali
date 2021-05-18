import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from config import config
from cali.lib.db import get_db
from cali.lib.credit import Credit

blueprint = Blueprint('credits', __name__, url_prefix='/credits')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    configuration = config.Config()
    if request.method == 'POST':
        credits = Credit.get_filtered_credits(request.form)
    else:
        credits = Credit.get_all_credits()

    Credit.update_credits_status(credits)
    return render_template('credits/search.html', credits=credits, configuration=configuration, Credit=Credit)


@blueprint.route('<int:id>/pay', methods=('GET','POST'))
def pay(id):
    configuration = config.Config()
    credit = Credit.get_credit_by_id(id)
    if request.method == 'POST':
        Credit.pay_credit(credit, request.form)
    return render_template('credits/pay.html', credit=credit, configuration=configuration)

