
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from cali.db import get_db

blueprint = Blueprint('users', __name__, url_prefix='/users')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    db = get_db()
    if request.method == 'POST':
        id = request.form['id']
        username = request.form['username']
        branch = request.form['branch']

        if id:
            users = db.execute("""
                     SELECT * FROM user
                     JOIN branch on user.branch_id = branch.id
                     WHERE user.id=?
                     """,
                    (int(id),)
                    ).fetchall()
            return render_template('users/search.html', users=users)

        elif username:
            users = db.execute("""
                        SELECT * FROM user
                        JOIN branch on user.branch_id = branch.id
                        WHERE username=?
                        """,
                        (username,)
                        ).fetchall()
            return render_template('users/search.html', users=users)

        else:
            users = db.execute("""
                        SELECT * FROM user
                        JOIN branch on user.branch_id = branch.id
                        WHERE branch_id=?
                        """,
                        (branch,)
                        ).fetchall()
            return render_template('users/search.html', users=users)

    users = db.execute("""
        SELECT * FROM user
        JOIN branch on user.branch_id = branch.id
        """
    ).fetchall()

    return render_template('users/search.html', users=users)

