from flask import redirect, url_for, request
from flask_login import current_user, login_required

from . import app


@app.get('/market/catalogue')
@login_required
def sell_catalogue():
    if current_user.is_authenticated():
        from jardiquest.model.path.market_model import display_sell_catalogue
        return display_sell_catalogue()
    else:
        return redirect(url_for('login'))



@app.get('/market/catalogue/<string:product>')
@login_required
def sell_product(product):
    if current_user.is_authenticated():
        from jardiquest.model.path.market_model import display_sell_product
        return display_sell_product(product)
    else:
        return redirect(url_for('login'))


@app.post('/market/catalogue/sell/<string:product>')
@login_required
def sell_product_post(product):
    quantity = float(request.form['sell_quantity'])
    cost = float(request.form['sell_price'])
    if current_user.is_authenticated():
        from jardiquest.model.path.market_model import sell_product
        return sell_product(product, quantity, cost)
    else:
        return redirect(url_for('login'))


@app.post('/market/catalogue/cancel/<string:selling>')
@login_required
def cancel_selling(selling):
    if current_user.is_authenticated():
        from jardiquest.model.path.market_model import cancel_selling
        return cancel_selling(selling)
    else:
        return redirect(url_for('login'))


@app.get('/market')
@login_required
def market():
    if current_user.is_authenticated():
        from jardiquest.model.path.market_model import display_market
        return display_market()
    else:
        return redirect(url_for('login'))


@app.get('/market/<string:product>')
@login_required
def market_product(product):
    if current_user.is_authenticated():
        from jardiquest.model.path.market_model import display_market_product
        return display_market_product(product)
    else:
        return redirect(url_for('login'))


@app.post('/market/<string:product>/buy')
@login_required
def market_buy(product):
    quantity = float(request.form['buy_quantity'])
    selling_id = request.form['selling_id']
    if current_user.is_authenticated():
        from jardiquest.model.path.market_model import market_buy
        return market_buy(quantity, selling_id)
    else:
        return redirect(url_for('login'))


@app.get('/market/orders')
@login_required
def display_orders():
    if current_user.is_authenticated():
        from jardiquest.model.path.market_model import display_orders
        return display_orders()
    else:
        return redirect(url_for('login'))


@app.post('/market/orders/<string:order_id>/confirm')
@login_required
def confirm_order(order_id):
    if current_user.is_authenticated():
        from jardiquest.model.path.market_model import confirm_order
        return confirm_order(order_id)
    else:
        return redirect(url_for('login'))

@app.get('/market/my_orders')
@login_required
def user_orders():
    if current_user.is_authenticated():
        from jardiquest.model.path.market_model import display_user_orders
        return display_user_orders()
    else:
        return redirect(url_for('login'))