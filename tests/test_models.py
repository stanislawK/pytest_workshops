from datetime import datetime, timedelta

import pytest

from app.models import DataModel, UserModel


@pytest.fixture
def new_user():
    return {
        "email": "test@test.com",
        "password": "pass123"
    }


def test_create_valid_user_model(new_user):
    """Test create new user with valid data."""
    user = UserModel(**new_user)

    assert user.email == new_user["email"]
    assert user.password != new_user["password"]
    assert user.check_password(new_user["password"])


@pytest.mark.parametrize("missing", ["email", "password"])
def test_create_user_model_with_missing_field(missing, new_user):
    """Test create new user with one field missing."""
    new_user.pop(missing)

    # Try create new model instance
    try:
        UserModel(**new_user)
    # Check error message
    except TypeError as err:
        assert "missing 1 required positional argument" in err.args[0]
        assert missing in err.args[0]


"""
@pytest.fixture
def new_data(): # That fixture is in conftest
    return {
        "value": 1000,
        "unit": "PLN",
        "user_id": 1
    }
"""


def test_create_valid_data_model(new_data):
    """Test create new data with valid data."""
    data = DataModel(**new_data)

    # Check if all values passed to model are correct
    for key, value in new_data.items():
        # These same as eg data.value == new_data["value"]
        assert getattr(data, key) == value

    # Then check created_on date (field added automatically)
    delta = timedelta(seconds=5)
    assert datetime.utcnow() - delta < data.created_on <= datetime.utcnow()
