import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask
)
from werkzeug.security import check_password_hash, generate_password_hash

from config import config
from cali.lib.db import get_db

blueprint = Blueprint('dashboard', __name__)

@blueprint.route('/')
def dashboard():
    configuration = config.Config()

    return render_template('dashboard/index.html', configuration=configuration)
