from http.client import HTTPException
import uuid
from datetime import date

from flask import abort, flash, request, render_template, redirect, url_for
from flask_login import current_user

from jardiquest.controller import handling_status_error
from jardiquest.model.database.entity.jardin import Jardin
from jardiquest.model.database.entity.user import User
from jardiquest.model.database.entity.quete import Quete
from jardiquest.setup_sql import db


def print_garden():
    jar = Jardin.query.filter_by(idJardin=current_user.idJardin).first()
    par = User.query.filter_by(idJardin=current_user.idJardin)
    if not jar:
        return render_template('handle_garden.html', jardin=jar, user=current_user, notexist=True)
    else:
        return render_template('handle_garden.html', jardin=jar, participant=par, user=current_user)


def handle_garden_handler_model(methods: str):
    user = User.query.filter_by(email=current_user.email).first()
    idJar = user.idJardin
    jardin = Jardin.query.filter_by(idJardin=idJar).first()
    if methods == 'put':
        name = request.form.get('name')
        moneyName = request.form.get('moneyName')
        return update_model_garden(jardin, name, moneyName)
    elif methods == 'delete':
        return delete_model_garden(jardin, user)
    else:
        return handling_status_error(HTTPException(404))


def update_model_garden(jardin: Jardin, name: str, nameMoney: str):
    if name is not None and nameMoney is not None:
        jardin.name = name
        jardin.moneyName = nameMoney
        db.session.commit()

    return redirect(url_for('controller.your_garden'))


def delete_model_garden(jardin: Jardin, user: User):
    user.idJardin = ""
    user.role = "Participant"
    db.session.delete(jardin)
    db.session.commit()
    return redirect(url_for('controller.garden'))


def add_garden_quest_print():
    idJar = current_user.idJardin
    jardin = Jardin.query.filter_by(idJardin=idJar).first()
    return render_template('create_quest.html', user=current_user, jardin=jardin)


def add_garden_quest(title: str, description: str, reward: int, duration: int, periodic: bool, start: str,
                     expiration: int):
    st = start.split("-")
    start = date(int(st[0]), int(st[1]), int(st[2]))
    if expiration is '':
        expiration = 1
    new_quest = Quete(idQuete=uuid.uuid1().hex, title=title, description=description,
                      periodicity=periodic,
                      estimatedTime=duration,
                      timeBeforeExpiration=expiration, reward=reward,
                      id_jardin=current_user.idJardin,
                      startingDate=start)
    db.session.add(new_quest)
    db.session.commit()
    return redirect(url_for("controller.your_garden"))
