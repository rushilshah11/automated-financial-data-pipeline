import pytest
from fastapi.testclient import TestClient
from tests.test_auth_flow import unique_email
from main import app


@pytest.fixture(scope="module")
def client():
    # TestClient will run FastAPI lifespan events (create_tables) when entered
    with TestClient(app) as c:
        yield c

def test_subscribe_list_and_unsubscribe(client: TestClient):
    # register and login to obtain token
    email = unique_email()
    password = "sub-test-pw"

    r = client.post("/auth/register", json={
        "first_name": "Sub",
        "last_name": "Tester",
        "email": email,
        "password": password,
    })
    assert r.status_code == 201

    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200
    token = r.json().get("token")
    assert token
    headers = {"Authorization": f"Bearer {token}"}

    # create subscription
    r = client.post("/subscriptions/", json={"ticker": "AAPL"}, headers=headers)
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["ticker"] == "AAPL"
    sub_id = body["id"]

    # list subscriptions
    r = client.get("/subscriptions/", headers=headers)
    assert r.status_code == 200
    arr = r.json()
    assert any(s["id"] == sub_id for s in arr)

    # unsubscribe
    r = client.delete(f"/subscriptions/AAPL", headers=headers)
    assert r.status_code == 200
    assert r.json().get("deleted", 0) >= 1

    # deleting again should return 404
    r = client.delete(f"/subscriptions/AAPL", headers=headers)
    assert r.status_code == 404
