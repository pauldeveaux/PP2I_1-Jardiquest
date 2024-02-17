from flask import request
from flask_login import login_required

from . import app


@app.get('/handle_garden')
@login_required
def your_garden():

    from jardiquest.model.path.handle_garden_model import print_garden
    return print_garden()


@app.post('/handle_garden')
@login_required
def post_garden():
    # handle case with put or delete methods
    methods = request.form.get('_method')
    from jardiquest.model.path.handle_garden_model import handle_garden_handler_model
    return handle_garden_handler_model(methods)

@app.get('/handle_garden/add_quest')
@login_required
def add_quest_garden():

    from jardiquest.model.path.handle_garden_model import add_garden_quest_print
    return add_garden_quest_print()

@app.post('/handle_garden/add_quest')
@login_required
def post_add_quest_garden():
    title = request.form['title']
    description = request.form['description']
    reward = request.form['sum']
    duration = request.form['duration']
    periodic = request.form.get('periodic') != None
    start = request.form['start']
    expiration = request.form['expiration']
    from jardiquest.model.path.handle_garden_model import add_garden_quest
    return add_garden_quest(title,description,reward,duration,periodic,start,expiration)