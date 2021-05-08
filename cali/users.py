import functools

from flask import (Blueprint, redirect, render_template, request, url_for)

from config import config
from cali.lib.user import User
from cali.lib.alert import Alert

blueprint = Blueprint('users', __name__, url_prefix='/users')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    configuration = config.Config()
    if request.method == 'POST':
        users = User.get_filtered_users(request.form)
    else:
        users = User.get_all_users()

    return render_template('users/search.html', users=users, configuration=configuration)

@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    configuration = config.Config()
    if request.method == 'POST':
        user = User(request.form)
        if user.is_valid():
            user.create_user()
            Alert.raise_success_alert('User Created')

    return render_template('users/create.html', configuration=configuration)


@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    User.delete_user(id)
    return redirect(url_for('users.search'))

@blueprint.route('<int:id>/update', methods=('GET', 'POST'))
def update(id):
    configuration = config.Config()
    if request.method == 'POST':
        user = User(request.form)
        user.update_user(id)
        Alert.raise_success_alert('User Updated')

    else:
        user = User.get_user_by_id(id)

    return render_template('users/update.html', user=user, configuration=configuration)
