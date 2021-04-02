
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from cali.db import get_all_users, search_users
from cali.lib.user import User

blueprint = Blueprint('users', __name__, url_prefix='/users')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    if request.method == 'POST':
        users = search_users(request.form) 
        return render_template('users/search.html', users=users)

    else:
        users = get_all_users()
        return render_template('users/search.html', users=users)

