
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

    # Check if date is 0
    for credit in credits:
        remainingTime = Credit.get_remaining_time(credit)
        Credit.return_overdue_credit_items(remainingTime, credit)
        Credit.save_overdue_credit_as_sale(remainingTime, credit)
        Credit.delete_credit(remainingTime, credit)

    # Check if it is fully payed

    return render_template('credits/search.html', credits=credits, configuration=configuration, Credit=Credit)



