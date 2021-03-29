import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from cali.db import get_db

blueprint = Blueprint('articles', __name__, url_prefix='/articles')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    db = get_db()

    articles = db.execute("""
        SELECT * FROM article
        JOIN category ON article.category_id = category.id
        """
    ).fetchall()

    return render_template('articles/search.html', articles=articles)

