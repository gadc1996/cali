import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from cali.db import get_db

blueprint = Blueprint('dashboard', __name__)

@blueprint.route('/')
def dashboard():
    return render_template('dashboard/index.html')
