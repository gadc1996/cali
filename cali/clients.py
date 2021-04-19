import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from config import config
from cali.lib.db import get_db
from cali.lib.client import Client, get_all_clients, get_filtered_clients, get_single_client, client_exist

blueprint = Blueprint('clients', __name__, url_prefix='/clients')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    configuration = config.Config()
    if request.method == 'POST':
        clients = get_filtered_clients(request.form) 
    else:
        clients = get_all_clients()

    return render_template('clients/search.html', clients=clients, configuration=configuration)

@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    configuration = config.Config()
    if request.method == 'POST':
        db = get_db()
        client = Client(request.form)

        if client_exist(client):
            g.message = 'Client Exists'
            g.messageColor = 'danger'
            return render_template('clients/create.html', configuration=configuration)
        else:
            g.message = 'Client Created'
            g.messageColor = 'success'
            db.execute(client.create_client())
            db.commit()
            return render_template('clients/create.html', configuration=configuration)

    return render_template('clients/create.html', configuration=configuration)

@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    db = get_db()
    client = Client(get_single_client(id))
    db.execute(client.delete_client(id))
    db.commit()

    return redirect(url_for('clients.search'))

@blueprint.route('<int:id>/update', methods=('GET', 'POST'))
def update(id):
    configuration = config.Config()
    if request.method == 'POST':
        db = get_db()
        client = Client(request.form)

        if client_exist(client):
            g.message = 'Client Exists'
            g.messageColor = 'danger'
            return render_template('clients/update.html', client=client, configuration=configuration)
        else:
            g.message = 'Client Updated'
            g.messageColor = 'success'
            db.execute(client.update_client(id))
            db.commit()
            return render_template('clients/update.html', client=client, configuration=configuration)
    else:
        client = get_single_client(id)
        return render_template('clients/update.html', client=client, configuration=configuration)
