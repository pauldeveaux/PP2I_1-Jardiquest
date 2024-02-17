from flask import redirect, url_for
from flask_login import current_user


def home_model():
    if current_user.is_authenticated:
        return redirect(url_for('controller.garden'))
    else:
        return redirect(url_for('controller.login'))
