import os

import pytest
from jardiquest.setup_sql import db
from jardiquest.setup_flask import create_app, ROOT_DIR


# Allow to not write the lines in the test_function everywhere but instead just pass testing_client in argument
@pytest.fixture(scope='module')
def app():
    flask_app = create_app(True)
    with flask_app.test_client() as app:
        with flask_app.app_context():
            yield app


@pytest.fixture(scope='class', autouse=True)
def database(app):
    f = open(os.path.join(ROOT_DIR, 'tests/dataset/dataset.sqlite'))
    db.create_all()
    for line in f.readlines():
        db.session.connection().execute(line)
        db.session.commit()
    f.close()
    yield db
    db.drop_all()
