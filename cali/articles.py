import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from cali.lib.db import get_db
from cali.lib.article import Article, get_all_articles, get_filtered_articles, get_single_article
from cali.lib.category import get_single_category, get_all_categories

blueprint = Blueprint('articles', __name__, url_prefix='/articles')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    if request.method == 'POST':
        articles = get_filtered_articles(request.form)
    else:
        articles = get_all_articles()

    return render_template('articles/search.html', articles=articles)


@blueprint.route('<int:id>/info', methods=('GET',))
def info(id):
        article = Article(get_single_article(id))
        return render_template('articles/info.html', article=article)

@blueprint.route('<int:id>/update', methods=('GET', 'POST'))
def update(id):
    if request.method == 'POST':
        db = get_db()
        article = Article(get_single_article(id))
        flash(article.article_exist())

        if article.article_exist():
            g.message = 'article Exists'
            g.messageColor = 'danger'
        else:
            g.message = 'article Updated'
            g.messageColor = 'success'
            db.execute(article.update_article())
            db.commit()
    else:
        article = Article(get_single_article(id))

    categories = get_all_categories()
    return render_template('articles/update.html', article=article, categories=categories)

@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        db = get_db()
        article = Article(request.form)

        if article.article_exist():
            g.message = 'article Exists'
            g.messageColor = 'danger'
        else:
            g.message = 'article Created'
            g.messageColor = 'success'
            flash(article.create_article())
            db.execute(article.create_article())
            db.commit()

    else:
        article = Article(get_single_article(1))

    categories = get_all_categories()
    return render_template('articles/create.html', categories=categories)


@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    db = get_db()
    article = Article(get_single_article(id))
    db.execute(article.delete_article())
    db.commit()
    return redirect(url_for('articles.search'))

