import os
import tempfile

import pytest

from app.app_factory import create_app
from app.extensions import db
from app.factories import DataFactory


@pytest.fixture
def app():
    """Create and configure a new app instance for tests."""
    # create a temp file to isolate the db for each test
    db_fd, db_path = tempfile.mkstemp()
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DATABASE'] = db_path
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

    # create the db and load test data
    with app.app_context():
        db.init_app(app)
        db.create_all()

    yield app

    # close and remove the temporary db
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def _db(app):
    with app.app_context():
        yield db


@pytest.fixture
def new_user():
    return {
        "email": "test@test.com",
        "password": "pass123"
    }


@pytest.fixture
def new_data():
    return {
        "value": 1000,
        "unit": "PLN",
        "user_id": 1
    }


@pytest.fixture
def registered_user(_db, client, new_user):
    client.post("/auth/register/", json=new_user)


@pytest.fixture
def token(client, registered_user, new_user):
    rv = client.post("/auth/login/", json=new_user)
    return rv.get_json()["access_token"]


@pytest.fixture
def add_data(app, _db, registered_user):
    DataFactory.create_batch(50)
