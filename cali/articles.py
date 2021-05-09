import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from config import config
from cali.lib.db import get_db
from cali.lib.article import Article, get_all_articles, get_filtered_articles, get_single_article
from cali.lib.category import Category

blueprint = Blueprint('articles', __name__, url_prefix='/articles')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    configuration = config.Config()
    if request.method == 'POST':
        articles = get_filtered_articles(request.form)
    else:
        articles = get_all_articles()

    return render_template('articles/search.html', articles=articles, configuration=configuration)


@blueprint.route('<int:id>/info', methods=('GET',))
def info(id):
    article = Article(get_single_article(id))
    configuration = config.Config()
    return render_template('articles/info.html', article=article, configuration=configuration)

@blueprint.route('<int:id>/update', methods=('GET', 'POST'))
def update(id):
    configuration = config.Config()
    article = Article(get_single_article(id))
    if request.method == 'POST':
        db = get_db()
        article.update_article(request.form)
        g.message = 'article Updated'
        g.messageColor = 'success'

    categories = Category.get_all_categories()
    return render_template('articles/update.html', article=article, categories=categories, configuration=configuration)

@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    configuration = config.Config()
    if request.method == 'POST':
        db = get_db()
        article = Article(request.form)

        if article.article_exist():
            g.message = 'article Exists'
            g.messageColor = 'danger'
        else:
            g.message = 'article Created'
            g.messageColor = 'success'
            db.execute(article.create_article())
            db.commit()

    categories = Category.get_all_categories()
    return render_template('articles/create.html', categories=categories, configuration=configuration)


@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    db = get_db()
    article = Article(get_single_article(id))
    db.execute(article.delete_article())
    db.commit()
    return redirect(url_for('articles.search'))

