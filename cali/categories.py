import functools

from flask import flash
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from config import config
from cali.lib.db import get_db
from cali.lib.category import Category
from cali.lib.alert import Alert

blueprint = Blueprint('categories', __name__, url_prefix='/categories')

@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    configuration = config.Config()
    if request.method == 'POST':
        category = Category(request.form)
        if category.is_valid():
            category.create_category()
            Alert.raise_success_alert('Category Created')

    return render_template('categories/create.html', configuration=configuration)

@blueprint.route('/search', methods=('GET','POST'))
def search():
    configuration = config.Config()
    if request.method == 'POST':
        categories = Category.get_filtered_categories(request.form)
    else:
        categories = Category.get_all_categories()

    return render_template('categories/search.html', categories=categories, configuration=configuration)


@blueprint.route('<int:id>/update', methods=('GET', 'POST'))
def update(id):
    configuration = config.Config()
    if request.method == 'POST':
        category = Category(request.form)
        if category.is_valid():
            category.update_category(id)
            Alert.raise_success_alert('Category Updated')
    else:
        category = Category.get_category_by_id(id)


    return render_template('categories/update.html', category=category, configuration=configuration)



@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    Category.delete_category(id)
    return redirect(url_for('categories.search'))

