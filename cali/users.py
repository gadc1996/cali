
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from cali.db import get_all_users, get_filtered_users, delete_user
from cali.lib.user import User

blueprint = Blueprint('users', __name__, url_prefix='/users')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    if request.method == 'POST':
        users = get_filtered_users(request.form) 
        return render_template('users/search.html', users=users)

    else:
        users = get_all_users()
        return render_template('users/search.html', users=users)

@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    delete_user(id)

    return redirect(url_for('users.search'))
