
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
    # if date is 0 remove the item
    for credit in credits:
        remainigTime = Credit.get_remaining_time(credit)
        if remainigTime == 30:

            # Delete credit
            # Save As sale
            # return items to inventory
            pass

    # Check if it is fully payed

    return render_template('credits/search.html', credits=credits, configuration=configuration, Credit=Credit)



