from jardiquest.setup_flask import create_app
from jardiquest.model.path.quest_model import *
from jardiquest.model.database.entity.quete import Quete
from jardiquest.model.database.entity.jardin import Jardin
from jardiquest.model.database.entity.user import User

import unittest



# file of tests for the quests

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
    def test_get_list_garden_quests(self):
        resp = self.app.get('/garden/quests', follow_redirects=True)
        assert(resp.request.path == '/login')

    def test_get_list_user_quests(self):
            resp = self.app.get('/my_quests', follow_redirects=True)
            assert(resp.request.path == '/login')
   
    def test_get_display_quest(self):
            resp = self.app.get('/quest/1', follow_redirects=True)
            assert(resp.request.path == '/login')

    # Post requests
    def test_post_accept_quest(self):
        resp = self.app.post('/quest/1/accept', follow_redirects=True)
        assert(resp.request.path == '/login')

    def test_post_cancel_quest(self):
            resp = self.app.post('/quest/1/cancel', follow_redirects=True)
            assert(resp.request.path == '/login')

    def test_post_complete_quest(self):
        resp = self.app.post('/quest/1/complete', follow_redirects=True)
        assert(resp.request.path == '/login')
   
   

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
    def test_get_list_garden_quests(self):
        resp = self.app.get('/garden/quests')
        assert (resp.status_code == 200)

    def test_get_list_user_quests(self):
            resp = self.app.get('my_quests')
            assert (resp.status_code == 200)
   
    def test_get_display__good_quest(self):
        resp = self.app.get('quest/1')
        assert (resp.status_code == 200)  

    def test_get_display_expired_quest(self):
        resp = self.app.get('quest/7')
        assert (resp.status_code == 403)  

    def test_get_display_another_garden_quest(self):
        resp = self.app.get('quest/4')
        assert (resp.status_code == 403)  

    # Post requests
    def test_post_accept_quest(self):
        resp = self.app.post('quest/1/accept')
        assert (resp.status_code == 302)

    def test_post_accept_quest_of_another_garden(self):
        resp = self.app.post('quest/4/accept')
        assert (resp.status_code == 403)

    def test_post_cancel_quest(self):
            resp = self.app.post('quest/1/cancel')
            assert (resp.status_code == 302)

    def test_post_cancel_quest_of_another_garden(self):
        resp = self.app.post('quest/4/cancel')
        assert (resp.status_code == 403)

    def test_post_complete_quest(self):
        resp = self.app.post('quest/1/accept')
        resp = self.app.post('quest/1/complete')
        assert (resp.status_code == 302)
