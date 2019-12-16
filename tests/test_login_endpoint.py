from http import HTTPStatus

import pytest


def test_login_valid_user(_db, client, registered_user, new_user):
    """Test login registered user with valid data."""
    rv = client.post("/auth/login/", json=new_user)
    response = rv.get_json()

    assert rv.status_code == HTTPStatus.OK
    assert response.get("access_token")


def test_login_unregistered_user(client, new_user):
    """Test login unregistered user."""
    rv = client.post("/auth/login/", json=new_user)
    response = rv.get_json()

    assert rv.status_code == HTTPStatus.UNAUTHORIZED
    assert response["message"] == "Invalid email or password"


def test_login_user_second_time(client, new_user, registered_user):
    """Test login user who is logged in already."""
    rv = client.post("/auth/login/", json=new_user)
    token = rv.get_json()["access_token"]
    rv = client.post(
        "/auth/login/",
        headers={"Authorization": "Bearer {}".format(token)},
        json=new_user
    )
    response = rv.get_json()
    assert rv.status_code == HTTPStatus.UNAUTHORIZED
    assert response["message"] == "User logged in already"


def test_login_user_with_wrong_password(client, new_user, registered_user):
    """Test login user with wrong password."""
    new_user["password"] = "wrong_password"
    rv = client.post("/auth/login/", json=new_user)

    response = rv.get_json()
    assert rv.status_code == HTTPStatus.UNAUTHORIZED
    assert response["message"] == "Invalid email or password"


@pytest.mark.parametrize("missing", ["password", "email"])
def test_login_user_with_missing_data(
    client, missing, new_user, registered_user
):
    """Test login user with one field missing."""
    new_user.pop(missing)
    rv = client.post("/auth/register/", json=new_user)
    response = rv.get_json()

    assert rv.status_code == HTTPStatus.BAD_REQUEST
    assert 'Missing data for required field.' in response[missing]
