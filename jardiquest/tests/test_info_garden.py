# make sur the path are good
def test_auth_controller(app):
    response = app.get('/garden')
    assert response.status_code == 302

    response = app.get('/new')
    assert response.status_code == 302

    response = app.get('/modify')
    assert response.status_code == 302
