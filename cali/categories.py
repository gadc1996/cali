
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from cali.lib.db import get_db
from cali.lib.category import Category, get_single_category, get_all_categories

blueprint = Blueprint('categories', __name__, url_prefix='/categories')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    if request.method == 'POST':
        categories = get_filtered_categories(request.form)
    else:
        categories = get_all_categories()

    return render_template('categories/search.html', categories=categories)


@blueprint.route('<int:id>/info', methods=('GET',))
def info(id):
        categorie = categorie(get_single_categorie(id))
        return render_template('categories/info.html', categorie=categorie)

@blueprint.route('<int:id>/update', methods=('GET', 'POST'))
def update(id):
    if request.method == 'POST':
        db = get_db()
        categorie = categorie(get_single_categorie(id))
        flash(categorie.categorie_exist())

        if categorie.categorie_exist():
            g.message = 'categorie Exists'
            g.messageColor = 'danger'
        else:
            g.message = 'categorie Updated'
            g.messageColor = 'success'
            db.execute(categorie.update_categorie())
            db.commit()
    else:
        categorie = categorie(get_single_categorie(id))

    categories = get_all_categories()
    return render_template('categories/update.html', categorie=categorie, categories=categories)

@blueprint.route('/create', methods=('GET', 'POST'))
def create():
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

    return render_template('categories/create.html')


@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    db = get_db()
    categorie = categorie(get_single_categorie(id))
    db.execute(categorie.delete_categorie())
    db.commit()
    return redirect(url_for('categories.search'))

