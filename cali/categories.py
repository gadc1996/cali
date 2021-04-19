import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from config import config
from cali.lib.db import get_db
from cali.lib.category import Category, get_single_category, get_all_categories

blueprint = Blueprint('categories', __name__, url_prefix='/categories')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    configuration = config.Config()
    if request.method == 'POST':
        pass
    #    categories = get_filtered_categories(request.form)
    categories = get_all_categories()
    return render_template('categories/search.html', categories=categories, configuration=configuration)

@blueprint.route('<int:id>/info', methods=('GET',))
def info(id):
    configuration = config.Config()
    category = Category(get_single_category(id))
    return render_template('categories/info.html',category=category, configuration=configuration)

@blueprint.route('<int:id>/update', methods=('GET', 'POST'))
def update(id):
    configuration = config.Config()
    if request.method == 'POST':
        db = get_db()
        category = Category(request.form)

        if category.category_exist():
            g.message = 'Category Exists'
            g.messageColor = 'danger'
        else:
            g.message = 'Category Updated'
            g.messageColor = 'success'
            db.execute(category.update_category(id))
            db.commit()
    else:
        category = Category(get_single_category(id))


    return render_template('categories/update.html', category=category, configuration=configuration)

@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    configuration = config.Config()
    if request.method == 'POST':
        db = get_db()
        category = Category(request.form)

        if category.category_exist():
            g.message = 'Category Exists'
            g.messageColor = 'danger'
        else:
            g.message = 'Category Created'
            g.messageColor = 'success'
            db.execute(category.create_category())
            db.commit()

    return render_template('categories/create.html', configuration=configuration)


@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    db = get_db()
    category = Category(get_single_category(id))
    db.execute(category.delete_category())
    db.commit()
    return redirect(url_for('categories.search'))

