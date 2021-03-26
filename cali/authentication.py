import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from cali.db import get_db

blueprint = Blueprint('authentication', __name__, url_prefix='/authentication')

@blueprint.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        database_query = """
        INSERT INTO user (username, password) VALUES(?, ?)
        """
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # data validation
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f'User {username} is already registered'

        if error is None:
            db.execute(
                database_query,
                (
                    username,
                    generate_password_hash(password)
                )
            )
            db.commit()
            return redirect(url_for('authentication.login'))

        flash(error)

    return render_template('authentication/register.html')

@blueprint.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?',
            (username,)
        ).fetchone()

        # data validation
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('hello'))

        flash(error)

    return render_template('authentication/login.html')

@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?',
            (user_id,)
        ).fetchone()

@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('hello'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('authentication.login'))

        return view(**kwargs)

    return wrapped_view
