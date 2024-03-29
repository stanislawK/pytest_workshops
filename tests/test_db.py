import pytest

from app.models import DataModel, UserModel


def test_save_user_to_db(_db, new_user):
    """Test save new user to db."""
    assert not _db.session.query(UserModel).all()

    user = UserModel(**new_user)
    _db.session.add(user)
    _db.session.commit()

    user_db = _db.session.query(UserModel).first()
    assert user_db == user


@pytest.fixture
def user_db(_db, new_user):
    user = UserModel(**new_user)
    _db.session.add(user)
    _db.session.commit()
    user_db = _db.session.query(UserModel).first()
    return user_db


def test_save_data_to_db(_db, new_data, user_db):
    """Test add new data model instance to db."""
    # Override fake user_id with id of user from db
    new_data["user_id"] == user_db.id
    data = DataModel(**new_data)
    _db.session.add(data)
    _db.session.commit()

    data_db = _db.session.query(DataModel).first()
    assert data_db == data


"""
from app.app_factory import create_app
from app.extensions import db

class TestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            'sqlite:///' + os.path.join(basedir, 'test.db')
        )
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
"""
