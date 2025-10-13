"""
Integration tests for auth flows (register, login, protected).

Assumptions/notes:
- Tests use a unique email per run to avoid collisions with existing data.
- Tests run against the same DB configured in settings. If you need
  isolated databases per test run consider wiring a test-specific DB URL.
"""

import time
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
def client():
    # TestClient will run FastAPI lifespan events (create_tables) when entered
    with TestClient(app) as c:
        yield c


def unique_email():
    # millisecond precision to avoid collisions in quick repeated runs
    return f"test.{int(time.time()*1000)}@example.com"


def test_register_success(client: TestClient):
    email = unique_email()
    resp = client.post(
        "/auth/register",
        json={
            "first_name": "Integration",
            "last_name": "Tester",
            "email": email,
            "password": "strongpassword123",
        },
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["email"] == email
    assert "id" in body


def test_register_duplicate_email(client: TestClient):
    email = unique_email()
    # first create
    r1 = client.post("/auth/register", json={
        "first_name": "Dup",
        "last_name": "User",
        "email": email,
        "password": "pw",
    })
    assert r1.status_code == 201
    # second create should fail with 400
    r2 = client.post("/auth/register", json={
        "first_name": "Dup2",
        "last_name": "User2",
        "email": email,
        "password": "pw2",
    })
    assert r2.status_code == 400
    assert "Email already registered" in r2.text


def test_login_success_and_protected(client: TestClient):
    email = unique_email()
    password = "secret-for-login"
    # register
    r = client.post("/auth/register", json={
        "first_name": "Log",
        "last_name": "Tester",
        "email": email,
        "password": password,
    })
    assert r.status_code == 201

    # login
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    body = r.json()
    # current implementation may differ; assert token present
    assert "token" in body
    token = body["token"]

    # protected success
    r = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text
    assert "data" in r.json()


def test_login_wrong_password(client: TestClient):
    email = unique_email()
    # create
    r = client.post("/auth/register", json={
        "first_name": "WP",
        "last_name": "Tester",
        "email": email,
        "password": "rightpwd",
    })
    assert r.status_code == 201

    # login with wrong password should return 400
    r = client.post("/auth/login", json={"email": email, "password": "wrongpwd"})
    assert r.status_code == 400
    assert "Invalid password" in r.text or "Invalid email or password" in r.text


def test_login_nonexistent_email(client: TestClient):
    r = client.post("/auth/login", json={"email": "no.such.user@example.com", "password": "pw"})
    assert r.status_code == 400
    assert "Invalid email or password" in r.text


def test_protected_missing_token(client: TestClient):
    r = client.get("/protected")
    assert r.status_code == 403


def test_protected_invalid_token(client: TestClient):
    r = client.get("/protected", headers={"Authorization": "Bearer invalid.token.here"})
    assert r.status_code == 401
