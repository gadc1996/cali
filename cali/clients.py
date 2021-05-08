from flask import ( Blueprint, redirect, render_template, request, url_for)

from config import config
from cali.lib.alert import Alert
from cali.lib.client import Client

blueprint = Blueprint('clients', __name__, url_prefix='/clients')

@blueprint.route('/search', methods=('GET','POST'))
def search():
    configuration = config.Config()
    if request.method == 'POST':
        clients = Client.get_filtered_clients(request.form)
    else:
        clients = Client.get_all_clients()

    return render_template('clients/search.html', clients=clients, configuration=configuration)

@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    configuration = config.Config()
    if request.method == 'POST':
        client = Client(request.form)
        if client.is_valid_create():
            client.create_client()
            Alert.raise_success_alert('Client Created')

    return render_template('clients/create.html', configuration=configuration)


@blueprint.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    Client.delete_client(id)
    return redirect(url_for('clients.search'))

@blueprint.route('<int:id>/update', methods=('GET', 'POST'))
def update(id):
    configuration = config.Config()
    if request.method == 'POST':
        client = Client(request.form)
        if client.is_valid_update():
            client.update_client(id)
            Alert.raise_success_alert('Client Updated')
    else:
        client = Client.get_client_by_id(id)

    return render_template('clients/update.html', client=client, configuration=configuration)
