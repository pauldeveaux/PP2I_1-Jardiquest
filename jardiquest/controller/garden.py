from flask_login import *

from . import app


# show all gardens
@app.route('/garden', methods=['GET', 'POST'])
@login_required
def garden():
    from jardiquest.model.path.garden_model import garden_model
    return garden_model()


# create a new garden (owner)
@app.route('/new', methods=['GET', 'POST'])
@login_required
def new_garden():
    from jardiquest.model.path.garden_model import new_garden_model
    return new_garden_model()


@app.route('/change/<choose>')
@login_required
def choose(choose):
    from jardiquest.model.path.garden_model import choose_model
    return choose_model(choose)


@app.route('/leave/<id>')
@login_required
def leave(id):
    from jardiquest.model.path.garden_model import leave_model
    return leave_model(id)


@app.route('/delete')
@login_required
def delete():
    from jardiquest.model.path.garden_model import delete_model
    return delete_model()


# create a new garden (owner)
@app.route('/modify', methods=['GET', 'POST'])
@login_required
def modify_garden():
    from jardiquest.model.path.garden_model import modify_garden_model
    return modify_garden_model()
