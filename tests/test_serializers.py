from marshmallow import ValidationError
import pytest

from app.models import DataModel
from app.serializers import DataSchema, UserSchema


def test_validate_correct_user_data(new_user):
    """Test loading schema with valid user data."""
    user_schema = UserSchema().load(new_user)

    # Check if schama was loaded correct
    assert user_schema["email"] == new_user["email"]
    assert user_schema["password"] == new_user["password"]


def test_validate_user_with_invalid_email(new_user):
    """Test loading schema with invalid email."""
    new_user["email"] = "it_is_not_an_email"
    # Try to load invalid user data to schema
    try:
        UserSchema().load(new_user)

    # Check if proper error was raised
    # Marshmallow will raise ValidationError exception if input is invalid
    # We can catch that exceprion, and check error message
    except ValidationError as err:
        """
        ValidationError in that example looks that:
        {
            "email": [
                "Not a valid email address."
            ]
        }
        """
        assert 'Not a valid email address.' in err.messages["email"]


def test_validate_user_with_invalid_password(new_user):
    """Test loading schema with too short password."""
    new_user["password"] = "test"
    # Try to load invalid user data to schema
    try:
        UserSchema().load(new_user)

    # Check if proper error was raised
    except ValidationError as err:
        assert 'Length must be between 5 and 70.' in err.messages["password"]


@pytest.mark.parametrize("missing", ["password", "email"])
def test_validate_user_with_missing_field(missing, new_user):
    """Test loading schema with one field missing."""
    new_user.pop(missing)
    # Try to load incomplete user data to schema
    try:
        UserSchema().load(new_user)

    # Check if proper error was raised
    except ValidationError as err:
        assert "Missing data for required field." in err.messages.get(missing)


def test_valiadate_correct_data(new_data):
    """Test loading schema with valid data."""
    new_data.pop("user_id")
    data_schema = DataSchema().load(new_data)

    # Check if schama was loaded correct
    for key, value in data_schema.items():
        assert new_data.get(key) == value


def test_dump_valid_data(new_data):
    """Test dumping schema with valid data."""
    data = DataModel(**new_data)
    data_schema = DataSchema().dump(data)

    # Check if created_at was dumped
    assert data_schema.get("created_on")
