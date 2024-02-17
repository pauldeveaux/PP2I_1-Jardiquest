
def test_auth_controller(app):
    response = app.get('/blog')
    assert response.status_code == 302

