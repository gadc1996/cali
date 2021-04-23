
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
        credits, filtered_credit = Credit.get_filtered_credits(request.form)
    else:
        credits, filtered_credit = Credit.get_all_credits()

    for credit in credits:
        remainingTime = Credit.get_remaining_time(credit)
        if remainingTime <= 0:
            Credit.return_overdue_credit_items(credit)
            Credit.save_credit_as_sale(credit)
            Credit.delete_credit(credit)

        if Credit.is_fully_payed(credit):
            Credit.save_credit_as_sale(credit)
            Credit.delete_credit(credit)

    return render_template('credits/search.html', credits=credits, configuration=configuration, Credit=Credit)


@blueprint.route('<int:id>/pay', methods=('GET','POST'))
def pay(id):
    configuration = config.Config()
    credit = Credit.get_single_credit(id)
    total = credit['total']
    payed = credit['payed']
    if request.method == 'POST':
        try:
            pay = int(request.form['pay'])
        except:
            pay = 0
        if Credit.is_pay_valid(total, payed, pay):
            payed += pay
            Credit.update_payed(id, payed)
        #credit = Credit.is_pay_valid(total, payed, pay)
        pass
    else:
        pass
    return render_template('credits/pay.html', credits=credits, configuration=configuration)

