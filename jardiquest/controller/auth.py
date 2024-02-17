from flask import request
from flask_login import login_required

from . import app


@app.get('/signup')
def signup():
    callback = request.args.get('next')
    email = request.args.get('email')
    name = request.args.get('name')

    from jardiquest.model.path.auth_model import signup_model
    return signup_model(callback, email, name)


@app.post('/signup')
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    callback = request.args.get('next')

    from jardiquest.model.path.auth_model import signup_post_model
    return signup_post_model(callback, email, name, password)


@app.get('/login')
def login():
    callback = request.args.get('next')
    email = request.args.get('email')

    from jardiquest.model.path.auth_model import login_model
    return login_model(callback, email)


@app.post('/login')
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    callback = request.args.get('next')

    from jardiquest.model.path.auth_model import login_post_model
    return login_post_model(email, password, callback)


@app.post('/logout')
@login_required
def logout():
    from jardiquest.model.path.auth_model import logout_model
    return logout_model()
