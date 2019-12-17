from http import HTTPStatus


def test_front_view(client):
    rv = client.get("/")
    response = rv.data

    assert rv.status_code == HTTPStatus.OK
    # assert response == "test"
    assert b"<h1>Hello test !!!</h1>" in response
