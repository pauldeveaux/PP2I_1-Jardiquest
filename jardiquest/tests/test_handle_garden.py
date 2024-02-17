# make sur the path are good
def test_auth_controller(app):
    response = app.get('/handle_garden')
    assert response.status_code == 302

    response = app.post('/handle_garden')
    assert response.status_code == 302

    response = app.get('/handle_garden/add_quest')
    assert response.status_code == 302

    response = app.post('/handle_garden/add_quest')
    assert response.status_code == 302
