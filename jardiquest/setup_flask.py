import os
from datetime import timedelta

import pandas as pd

from flask import Flask, session, redirect, url_for, flash, request
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException

from jardiquest import controller, model
from jardiquest.controller import handling_status_error
from jardiquest.model.database.entity.user import User
from jardiquest.model.database.entity.catalogue import Catalogue
from jardiquest.setup_sql import db, database_path, database_path_test

# do not remove this import allows SQLAlchemy to find the table
from jardiquest.model.database.entity import annonce, catalogue, jardin, quete, recolte, commande

from flask_apscheduler import APScheduler
from jardiquest.model.database.entity.quete import update_quests

# To find the root of the project everywhere
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# To restrict the format of file being upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'jardiquest/static/upload'

# create the flask app (useful to be separate from the app.py
# to be used in the test and to put all the code in the jardiquest folder


def create_app(test):
    if test:
        db_path = 'sqlite://' + database_path_test
    else:
        db_path = 'sqlite://' + database_path


    size_limit_mo = 10

    # config the app to make app.py the start point but the actual program is one directory lower
    flask_serv_intern = Flask(__name__,
                              static_folder="static",
                              template_folder='view')

    flask_serv_intern.config['SQLALCHEMY_DATABASE_URI'] = db_path
    flask_serv_intern.config['SECRET_KEY'] = '=xyb3y=2+z-kd!3rit)hfrg0j!e!oggyny0$5bliwlb8v76j'
    flask_serv_intern.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    flask_serv_intern.config['MAX_CONTENT_LENGTH'] = size_limit_mo * 1024 * 1024

    flask_serv_intern.register_blueprint(controller.app)
    flask_serv_intern.register_error_handler(HTTPException, handling_status_error)
    db.init_app(flask_serv_intern)
    with flask_serv_intern.app_context():
        db.create_all()

        if db.session.query(Catalogue).first() is None:
            df = pd.read_csv(os.path.join(ROOT_DIR, '../data_vegetables/data_recoltes.csv'), sep=";", header=0)
            df.to_sql('catalogue', db.engine, if_exists="append", index=False)


    # Scheduler each day
    scheduler = APScheduler()
    scheduler.init_app(flask_serv_intern)

    @scheduler.task("interval",hours=24)  
    def update_state_quests():
        update_quests(scheduler.app)
 
    scheduler.start()   


    # login handling
    login_manager = LoginManager()
    login_manager.login_view = 'controller.login'
    login_manager.init_app(flask_serv_intern)
    login_manager.refresh_view = 'controller.login'

    login_manager.needs_refresh_message = u"Session expirée, veuillez vous reconnecter"
    login_manager.needs_refresh_message_category = "info"     


    @login_manager.unauthorized_handler
    def unauthorized_callback():
        flash("Veuillez vous connecter pour accéder à ce contenu")
        return redirect(url_for('controller.login', next=request.url))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # all operation of closing ressources like database
    @flask_serv_intern.teardown_appcontext
    def close_ressource(exception):
        model.close_connection(exception)

    @flask_serv_intern.before_request
    def before_request():
        session.permanent = True
        flask_serv_intern.permanent_session_lifetime = timedelta(hours=4)

    return flask_serv_intern
