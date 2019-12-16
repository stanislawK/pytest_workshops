from http import HTTPStatus

from flask_jwt_extended import jwt_required
import pytest


@pytest.fixture
def protected(app):
    @app.route("/test")
    @jwt_required
    def protected():
        return "Proteced route"


def test_logout_user(client, token):
    """Test logout logged in user."""
    rv = client.delete(
        "/auth/logout/",
        headers={"Authorization": "Bearer {}".format(token)}
    )
    response = rv.get_json()

    assert rv.status_code == HTTPStatus.OK
    assert response["message"] == "Successfully logged out"


def test_protected_route_after_logout(app, protected, client, token):
    """Test reach protected route after logout."""
    client.delete(
        "/auth/logout/",
        headers={"Authorization": "Bearer {}".format(token)}
    )
    rv = client.get(
        "/test", headers={"Authorization": "Bearer {}".format(token)}
    )
    response = rv.get_json()
    assert rv.status_code == HTTPStatus.UNAUTHORIZED
    assert response['msg'] == 'Token has been revoked'
