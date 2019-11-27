import os
import tempfile

import pytest

from app.app_factory import create_app
from app.extensions import db


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
