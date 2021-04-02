import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as file:
        db.executescript(file.read().decode())

def get_single_user(id):
    db = get_db()
    user = db.execute(f'SELECT username, password, is_super, can_discount, branch_id FROM user JOIN branch on user.branch_id = branch.id WHERE user.id={id}').fetchone()
    return user

def get_all_users():
    db = get_db()
    users = db.execute("""
        SELECT * FROM user
        JOIN branch on user.branch_id = branch.id
        """
    ).fetchall()
    return users

def get_filtered_users(form):
    db = get_db()
    for key,value in form.items():
        if value is '':
            continue

        if key =='id':
            users = db.execute('SELECT * FROM user '
                'JOIN branch on user.branch_id = branch.id '
                f'WHERE user.{key}={value}'
                ).fetchall()
            return users

        else:
            users = db.execute('SELECT * FROM user '
                'JOIN branch on user.branch_id = branch.id '
                f'WHERE user.{key}="{value}" '
                ).fetchall()
            return users

def delete_user(id):
    db = get_db()
    db.execute(f'DELETE FROM user WHERE id={id}')
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    click.echo('Database Initialized')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
