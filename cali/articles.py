import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from config import config
from cali.lib.db import get_db
from cali.lib.article import Article 
from cali.lib.category import Category
from cali.lib.alert import Alert

blueprint = Blueprint('articles', __name__, url_prefix='/articles')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    configuration = config.Config()
    if request.method == 'POST':
        articles = Article.get_filtered_articles(request.form)
    else:
        articles = Article.get_all_articles()

    return render_template('articles/search.html', articles=articles, configuration=configuration)

@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    configuration = config.Config()
    if request.method == 'POST':
        article = Article(request.form)
        if article._is_valid():
            article.create_article()
            Alert.raise_success_alert('Article Created')
    categories = Category.get_all_categories()

    return render_template('articles/create.html', categories=categories, configuration=configuration)

@blueprint.route('<int:id>/info', methods=('GET',))
def info(id):
    configuration = config.Config()
    article = Article.get_article_by_id(id)
    
    return render_template('articles/info.html', article=article, configuration=configuration)

@blueprint.route('<int:id>/update', methods=('GET', 'POST'))
def update(id):
    configuration = config.Config()
    article = Article.get_article_by_id(id)
    if request.method == 'POST':
        article = Article(request.form)
        article.update_article(id)
        Alert.raise_success_alert('Article Updated')

    categories = Category.get_all_categories()

    return render_template('articles/update.html', article=article, categories=categories, configuration=configuration)



@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    Article.delete_article(id)
    return redirect(url_for('articles.search'))

