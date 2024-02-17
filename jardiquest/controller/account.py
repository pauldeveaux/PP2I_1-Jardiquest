from flask import request

from jardiquest.controller import app


@app.post("/account")
def account_handler():
    # handle case with put or delete methods
    methods = request.form.get('_method')
    from jardiquest.model.path.account_model import account_handler_model
    return account_handler_model(methods)
