import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from config import config
from cali.lib.db import get_db
from cali.lib.user import User, get_all_users, get_filtered_users, get_single_user, user_exist

blueprint = Blueprint('users', __name__, url_prefix='/users')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    configuration = config.Config()
    if request.method == 'POST':
        users = get_filtered_users(request.form) 
    else:
        users = get_all_users()

    return render_template('users/search.html', users=users, configuration=configuration)

@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    configuration = config.Config()
    if request.method == 'POST':
        db = get_db()
        user = User(request.form)

        if user_exist(user):
            g.message = 'User Exists'
            g.messageColor = 'danger'
            return render_template('users/create.html', configuration=configuration)
        else:
            g.message = 'User Created'
            g.messageColor = 'success'
            db.execute(user.create_user())
            db.commit()
            return render_template('users/create.html', configuration=configuration)

    return render_template('users/create.html', configuration=configuration)

@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    db = get_db()
    user = User(get_single_user(id))
    db.execute(user.delete_user(id))
    db.commit()

    return redirect(url_for('users.search'))

@blueprint.route('<int:id>/update', methods=('GET', 'POST'))
def update(id):
    configuration = config.Config()

    if request.method == 'POST':
        db = get_db()
        user = User(request.form)

        if user_exist(user):
            g.message = 'User Exists'
            g.messageColor = 'danger'
            return render_template('users/update.html', user=user, configuration=configuration)
        else:
            g.message = 'User Updated'
            g.messageColor = 'success'
            db.execute(user.update_user(id))
            db.commit()
            return render_template('users/update.html', user=user, configuration=configuration)
    else:
        user = get_single_user(id)
        return render_template('users/update.html', user=user, configuration=configuration)
