from flask_login import *

from . import app


@app.route('/suggestion', methods=['GET', 'POST'])
@login_required
def suggestion():
    from jardiquest.model.path.suggestion_model import suggestion_model
    return suggestion_model()


@app.route('/buy/<numbs>/<ids>')
@login_required
def buy(numbs, ids):
    from jardiquest.model.path.suggestion_model import buy_model
    return buy_model(numbs, ids)