from flask import request, render_template
from flask_login import current_user
from sqlalchemy import desc

from jardiquest.model.database.entity.annonce import Annonce
from jardiquest.setup_sql import db


def render_blog():
    anon = Annonce.query.filter_by(idJardin=current_user.idJardin).order_by(desc("idAnnonce"))
    return render_template('blog.html', user=current_user, messages=anon)


def add_new_message():
    msg = request.form['msg']
    anon = Annonce.query.order_by(desc("idAnnonce")).first()
    if anon is None:
        id = 0
    else:
        id = anon.idAnnonce + 1
    new_msg = Annonce(id, msg, current_user)
    db.session.add(new_msg)
    db.session.commit()
    return render_blog()
