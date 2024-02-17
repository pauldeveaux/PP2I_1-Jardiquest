from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from jardiquest.model.database.entity.user import User
from jardiquest.setup_sql import db


def signup_model(callback=None, email=None, name=None):
    if callback is None:
        callback = ''
    else:
        callback = "?next=" + callback
    return render_template('signup.html', callback=callback, email=email, name=name)


def signup_post_model(callback=None, email=None, name=None, password=None):
    user = User.query.filter_by(email=email).first()

    is_valid = User.is_valid_commit(email, name, password)

    if user:
        flash('L\'email existe déjà')
        return redirect(url_for('controller.signup', next=callback, email=email, name=name))

    if type(is_valid) is not bool:
        flash(is_valid)
        return redirect(url_for('controller.signup', next=callback, email=email, name=name))

    new_user = User(email=email, name=name, password=password)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('controller.login', next=callback))


def login_model(callback=None, email=None):
    if callback is None:
        callback = ''
    else:
        callback = "?next=" + callback
    return render_template('login.html', callback=callback, email=email)


def login_post_model(email, password, callback=None):
    if email == '':
        flash('Veuillez rentrer votre e-mail')
        return redirect(url_for('controller.login', next=callback))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('Email inconnu')
        return redirect(url_for('controller.login', next=callback, email=email))
    if not check_password_hash(user.password, password):
        flash('Mot de passe incorrect')
        return redirect(url_for('controller.login', next=callback, email=email))

    login_user(user)

    if callback is not None:
        return redirect(callback)

    return redirect(url_for('controller.profile'))


def logout_model():
    logout_user()
    return redirect(url_for('controller.login'))
