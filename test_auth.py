import pytest
from app import app, users, login_attempts


@pytest.fixture
def client():
    app.config["TESTING"] = True

    users.clear()
    login_attempts.clear()

    with app.test_client() as client:
        yield client


def register_user(client, username="testuser", password="TestPassword123!"):
    return client.post(
        "/register",
        json={
            "username": username,
            "password": password,
        },
    )


def test_password_is_hashed(client):
    response = register_user(client)

    assert response.status_code == 201
    assert users["testuser"] != "TestPassword123!"


def test_invalid_registration_is_rejected(client):
    response = client.post(
        "/register",
        json={
            "username": "x",
            "password": "123",
        },
    )

    assert response.status_code == 400


def test_successful_login(client):
    register_user(client)

    response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 200


def test_wrong_password_returns_generic_error(client):
    register_user(client)

    response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json["error"] == "Invalid username or password"


def test_unknown_user_has_generic_error(client):
    response = client.post(
        "/login",
        json={
            "username": "unknown",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json["error"] == "Invalid username or password"


def test_rate_limit(client):
    register_user(client)

    for _ in range(5):
        response = client.post(
            "/login",
            json={
                "username": "testuser",
                "password": "WrongPassword123!",
            },
        )
        assert response.status_code == 401

    response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 429


def test_protected_route_requires_login(client):
    response = client.get("/profile")

    assert response.status_code == 401


def test_logout(client):
    register_user(client)

    client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "TestPassword123!",
        },
    )

    response = client.post("/logout")

    assert response.status_code == 200

    response = client.get("/profile")

    assert response.status_code == 401


def test_session_cookie_security_settings():
    assert app.config["SESSION_COOKIE_HTTPONLY"] is True
    assert app.config["SESSION_COOKIE_SECURE"] is True
    assert app.config["SESSION_COOKIE_SAMESITE"] == "Lax"
