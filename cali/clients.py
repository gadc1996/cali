import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from cali.db import get_db, get_all_clients, get_filtered_clients, get_single_client, client_exist
from cali.lib.client import Client

blueprint = Blueprint('clients', __name__, url_prefix='/clients')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    if request.method == 'POST':
        clients = get_filtered_clients(request.form) 
        return render_template('clients/search.html', clients=clients)
    else:
        clients = get_all_clients()
        return render_template('clients/search.html', clients=clients)

@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        db = get_db()
        client = Client(request.form)

        if client_exist(client):
            g.message = 'Client Exists'
            g.messageColor = 'danger'
            return render_template('clients/create.html')
        else:
            g.message = 'Client Created'
            g.messageColor = 'success'
            db.execute(client.create_client())
            db.commit()
            return render_template('clients/create.html')

    return render_template('clients/create.html')

@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    db = get_db()
    client = Client(get_single_client(id))
    db.execute(client.delete_client(id))
    db.commit()

    return redirect(url_for('clients.search'))

@blueprint.route('<int:id>/update', methods=('GET', 'POST'))
def update(id):
    if request.method == 'POST':
        db = get_db()
        client = Client(request.form)

        if client_exist(client):
            g.message = 'Client Exists'
            g.messageColor = 'danger'
            return render_template('clients/update.html', client=client)
        else:
            g.message = 'Client Updated'
            g.messageColor = 'success'
            db.execute(client.update_client(id))
            db.commit()
            return render_template('clients/update.html', client=client)
    else:
        client = get_single_client(id)
        return render_template('clients/update.html', client=client)
