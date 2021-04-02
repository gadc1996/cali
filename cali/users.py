import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from cali.db import get_db, get_all_users, get_filtered_users, delete_user, get_single_user
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

@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        db = get_db()
        user = User(request.form)
        db.execute(user.create_user())
        db.commit()
        return redirect(url_for('users.search'))

    return render_template('users/create.html')

@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    db = get_db()
    user = User(get_single_user(id))
    db.execute(user.delete_user(id))
    db.commit()

    return redirect(url_for('users.search'))

@blueprint.route('<int:id>/update', methods=('GET', 'POST'))
def update(id):
    if request.method == 'POST':
        db = get_db()
        user = User(request.form)
        db.execute(user.update_user(id))
        db.commit()
    else:
        user = get_single_user(id)

    return render_template('users/update.html', user=user)
