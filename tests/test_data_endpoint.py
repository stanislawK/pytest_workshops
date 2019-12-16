from http import HTTPStatus

from app.models import DataModel


def test_add_new_data(_db, client, token):
    """Test add new DataModel instance."""
    rv = client.post(
        "/data/",
        json={"value": 1000, "unit": "PLN"},
        headers={"Authorization": "Bearer {}".format(token)}
    )
    response = rv.get_json()
    assert rv.status_code == HTTPStatus.CREATED
    assert response["value"] == 1000

    # Check if datetime was added
    assert response.get("created_on")

    # Check if data was added to db
    assert _db.session.query(DataModel).first()


def test_get_data(_db, client, token, add_data):
    """Test get data endpoint."""
    rv = client.get(
        "/data/",
        headers={"Authorization": "Bearer {}".format(token)}
    )
    response = rv.get_json()
    assert rv.status_code == HTTPStatus.OK
    assert len(response) == 50
