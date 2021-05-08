import functools

from flask import (Blueprint, g, redirect, render_template, request, session, url_for)

from config import config
from cali.lib.db import get_db
from cali.lib.user import User

blueprint = Blueprint('authentication', __name__, url_prefix='/authentication')

@blueprint.route('/login', methods=('GET', 'POST'))
def login():
    configuration = config.Config()

    if request.method == 'POST':
        User.log_in_user(request.form)
        return redirect(url_for('index'))

    else:
        return render_template('authentication/login.html', configuration=configuration)

@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.get_user_by_id(user_id)


