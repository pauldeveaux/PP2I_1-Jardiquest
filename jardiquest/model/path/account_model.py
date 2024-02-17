from http.client import HTTPException

from flask import request, redirect, url_for, flash
from flask_login import current_user

from jardiquest.controller import handling_status_error, logout
from jardiquest.model.database.entity.user import User
from jardiquest.setup_sql import db


def account_handler_model(methods: str):
    user = current_user

    if methods == 'put':
        email = user.email
        name = request.form.get('name')
        new_password = request.form.get('new_password')
        return update_account_model(user, email, name, new_password)
    elif methods == 'delete':
        return delete_account_model(user)
    else:
        return handling_status_error(HTTPException(404))


def update_account_model(user: User, email: str, name: str, new_password: str):

    if new_password != "" and new_password is not None:
        user.update_password(new_password)
        is_valid = User.is_valid_commit(email, name, new_password)
    else:
        is_valid = User.is_valid_commit_email_name(email, name)

    if type(is_valid) is not bool:
        flash(is_valid)
        return redirect(url_for('controller.profile'))

    user.email = email
    user.name = name
    db.session.commit()

    return redirect(url_for('controller.profile'))


def delete_account_model(user: User):
    db.session.delete(user)
    db.session.commit()
    flash("Compte supprimé avec succès")
    return logout()
