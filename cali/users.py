
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from cali.db import get_db

blueprint = Blueprint('users', __name__, url_prefix='/users')

@blueprint.route('/search', methods=('GET',))
def search():
    db = get_db()
    users = db.execute(
        'SELECT * FROM user'
    ).fetchall()

    # data validation
    return render_template('users/search.html', users=users)

