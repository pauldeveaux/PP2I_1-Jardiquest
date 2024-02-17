import unittest

from jardiquest.model.path.auth_model import *
from jardiquest.setup_flask import create_app


# file of test for the auth
# controller and model part


# make sur the path are good
def test_auth_controller(app):
    response = app.get('/login')
    assert response.status_code == 200

    response = app.get('/signup')
    assert response.status_code == 200

    response = app.post('/login')
    assert response.status_code == 302

    response = app.post('/signup')
    assert response.status_code == 302

    response = app.get('/logout')
    assert response.status_code == 405


class TestUserNotLogged(unittest.TestCase):
    @classmethod
    def setup_class(self):
        app = create_app(True)
        db.app = app
        self.app = app.test_client()

    # Gets requests
    def test_redirection(self):
        resp = self.app.get('/garden', follow_redirects=True)
        assert(resp.request.path == '/login')
        resp = self.app.get('/garden/quests', follow_redirects=True)
        assert(resp.request.path == '/login')
        resp = self.app.get('/market', follow_redirects=True)
        assert(resp.request.path == '/login')


class TestUserLogged(unittest.TestCase):

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.post('/logout')

    @classmethod
    def setup_class(self):
        app = create_app(True)
        db.app = app
        self.app = app.test_client()
        self.login(self, "b@gmail.com", "azertyui")

    def test_login(self):
        resp = self.login("b@gmail.com", "azertyui")
        assert resp.status_code == 200

    def test_logout(self):
        self.login("b@gmail.com", "azertyui")
        resp = self.logout()
        assert resp.status_code == 302
        resp = self.app.get('/garden', follow_redirects=True)
        assert(resp.request.path == '/login')

    def test_garden(self):
        user = User.query.filter_by(email="b@gmail.com").first()
        assert user.idJardin == '1'

    # Gets requests
    def test_redirection(self):
        self.login("b@gmail.com", "azertyui")
        resp = self.app.get('/garden', follow_redirects=True)
        assert(resp.request.path == '/garden')
        resp = self.app.get('/garden/quests', follow_redirects=True)
        assert(resp.request.path == '/garden/quests')
        resp = self.app.get('/market', follow_redirects=True)
        assert(resp.request.path == '/market')
