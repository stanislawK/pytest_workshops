import pytest

from app.models import UserModel


@pytest.fixture
def new_user():
    return {
        "email": "test@test.com",
        "password": "pass123"
    }


def test_create_valid_user_model(new_user):
    user = UserModel(**new_user)

    assert user.email == new_user["email"]
    assert user.password != new_user["password"]
    assert user.check_password(new_user["password"])


@pytest.mark.parametrize("missing", ["email", "password"])
def test_create_user_model_with_missing_field(missing, new_user):
    new_user.pop(missing)
    try:
        UserModel(**new_user)
    except TypeError as err:
        assert "missing 1 required positional argument" in err.args[0]
        assert missing in err.args[0]
