from flask import (Blueprint, g, redirect, render_template, url_for)

from config import config
from cali.lib.alert import Alert

blueprint = Blueprint('dashboard', __name__)

@blueprint.route('/')
def dashboard():
    configuration = config.Config()

    if g.user is None:
        Alert.raise_danger_alert('Not Logged In')
        return redirect(url_for('authentication.login'))

    else:
        return render_template('dashboard/index.html', configuration=configuration)

