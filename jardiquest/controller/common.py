from flask import render_template
from flask_login import current_user, login_required

from jardiquest.controller import app


@app.get('/')
def home():
    from jardiquest.model.path.common_model import home_model
    return home_model()


@app.get('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

