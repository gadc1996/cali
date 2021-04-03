import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from cali.lib.db import get_db
from cali.lib.article import get_all_articles, get_filtered_articles

blueprint = Blueprint('articles', __name__, url_prefix='/articles')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    if request.method == 'POST':
        articles = get_filtered_articles(request.form)
    else:
        articles = get_all_articles()

    return render_template('articles/search.html', articles=articles)


@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        db = get_db()
        user = User(request.form)

        if user_exist(user):
            g.message = 'User Exists'
            g.messageColor = 'danger'
            return render_template('users/create.html')
        else:
            g.message = 'User Created'
            g.messageColor = 'success'
            db.execute(user.create_user())
            db.commit()
            return render_template('users/create.html')

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

        if user_exist(user):
            g.message = 'User Exists'
            g.messageColor = 'danger'
            return render_template('users/update.html', user=user)
        else:
            g.message = 'User Updated'
            g.messageColor = 'success'
            db.execute(user.update_user(id))
            db.commit()
            return render_template('users/update.html', user=user)
    else:
        user = get_single_user(id)
        return render_template('users/update.html', user=user)
