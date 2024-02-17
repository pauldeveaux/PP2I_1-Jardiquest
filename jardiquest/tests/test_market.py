from jardiquest.setup_flask import create_app
from jardiquest.model.path.market_model import *
from jardiquest.model.database.entity.user import User

import unittest


# file of tests for the market

class TestUserNotLogged(unittest.TestCase):
    @classmethod
    def setup_class(self):
        app = create_app(True)
        db.app = app
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    @classmethod
    def teardown_class(self):
        self.app_context.pop()

    # Gets requests
    def test_get_catalogue(self):
        resp = self.app.get('/market/catalogue')
        assert (resp.status_code == 302)

    def test_get_sell_product(self):
        resp = self.app.get('/market/catalogue/1')
        assert (resp.status_code == 302)

    def test_get_market(self):
        resp = self.app.get('/market')
        assert (resp.status_code == 302)

    def test_get_market_product(self):
        resp = self.app.get('/market/product')
        assert (resp.status_code == 302)

    def test_get_orders(self):
        resp = self.app.get('/market/orders')
        assert (resp.status_code == 302)

    # Posts requests
    def test_post_sell_product(self):
        resp = self.app.post('/market/catalogue/sell/product')
        assert (resp.status_code == 302)

    def test_post_cancel_selling(self):
        resp = self.app.post('/market/catalogue/cancel/selling')
        assert (resp.status_code == 302)

    def test_post_buy_product(self):
        resp = self.app.post('/market/product/buy')
        assert (resp.status_code == 302)

    def test_post_confirm_order(self):
        resp = self.app.post('/market/orders/1/confirm')
        assert (resp.status_code == 302)


class TestUserParticipant(unittest.TestCase):
    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def register_user(self, username, email, password):
        return self.app.post('/register', data=dict(
            username=username,
            email=email,
            password=password,
        ), follow_redirects=True)

    @classmethod
    def setup_class(self):
        app = create_app(True)
        db.app = app
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        self.login(self, "b@gmail.com", "azertyui")

    @classmethod
    def teardown_class(self):
        self.app_context.pop()

    def test_login(self):
        resp = self.login("b@gmail.com", "azertyui")
        assert resp.status_code == 200

    def test_garden(self):
        user = User.query.filter_by(email="b@gmail.com").first()
        assert user.idJardin == '1'

    # Gets requests
    def test_get_catalogue(self):
        resp = self.app.get('/market/catalogue')
        assert (resp.status_code == 403)

    def test_get_sell_product(self):
        resp = self.app.get('/market/catalogue/1')
        assert (resp.status_code == 403)

    def test_get_market(self):
        resp = self.app.get('/market')
        assert (resp.status_code == 200)

    def test_get_market_product(self):
        resp = self.app.get('/market/Abricot')
        assert (resp.status_code == 200)

    def test_get_orders(self):
        resp = self.app.get('/market/orders')
        assert (resp.status_code == 403)

    # Posts requests
    def test_post_sell_product(self):
        resp = self.app.post('/market/catalogue/sell/Abricot', data=dict(sell_quantity=1, sell_price=1))
        assert (resp.status_code == 403)

    def test_post_cancel_selling(self):
        resp = self.app.post('/market/catalogue/cancel/1')
        assert (resp.status_code == 403)

    def test_post_buy_product(self):
        resp = self.app.post('/market/Abricot/buy', data=dict(buy_quantity=1, selling_id='adba2'))
        assert (resp.status_code == 302)

    def test_post_confirm_order(self):
        resp = self.app.post('/market/orders/abcdef/confirm')
        assert (resp.status_code == 403)


class TestUserGerant(unittest.TestCase):
    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def register_user(self, username, email, password):
        return self.app.post('/register', data=dict(
            username=username,
            email=email,
            password=password,
        ), follow_redirects=True)

    @classmethod
    def setup_class(self):
        app = create_app(True)
        db.app = app
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        self.login(self, "a@gmail.com", "azertyui")

    @classmethod
    def teardown_class(self):
        self.app_context.pop()

    def test_login(self):
        resp = self.login("a@gmail.com", "azertyui")
        assert resp.status_code == 200

    def test_garden(self):
        user = User.query.filter_by(email="a@gmail.com").first()
        assert user.idJardin == '1'

    # Gets requests
    def test_get_catalogue(self):
        resp = self.app.get('/market/catalogue')
        assert (resp.status_code == 200)

    def test_get_sell_product(self):
        resp = self.app.get('/market/catalogue/Abricot')
        assert (resp.status_code == 200)

    def test_get_market(self):
        resp = self.app.get('/market')
        assert (resp.status_code == 200)

    def test_get_market_product(self):
        resp = self.app.get('/market/Abricot')
        assert (resp.status_code == 200)

    def test_get_orders(self):
        resp = self.app.get('/market/orders')
        assert (resp.status_code == 200)

    # Posts requests
    def test_post_sell_product(self):
        resp = self.app.post('/market/catalogue/sell/Abricot', data=dict(sell_quantity=1, sell_price=1))
        assert (resp.status_code == 302)

    def test_post_cancel_selling(self):
        resp = self.app.post('/market/catalogue/cancel/adbaze2')
        assert (resp.status_code == 302)

    def test_post_buy_product(self):
        resp = self.app.post('/market/Abricot/buy', data=dict(buy_quantity=1, selling_id='adba2'))
        assert (resp.status_code == 302)

    def test_post_confirm_order(self):
        resp = self.app.post('/market/orders/abcdef/confirm')
        assert (resp.status_code == 302)
