import pytest


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
