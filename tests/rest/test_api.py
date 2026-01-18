from app.api import app


def test_sum_ok():
    client = app.test_client()
    response = client.get("/sum?a=2&b=3")
    assert response.status_code == 200
    assert response.json["result"] == 5


def test_sub_ok():
    client = app.test_client()
    response = client.get("/sub?a=10&b=4")
    assert response.status_code == 200
    assert response.json["result"] == 6


def test_bad_params():
    client = app.test_client()
    response = client.get("/sum?a=x&b=1")
    assert response.status_code == 400
