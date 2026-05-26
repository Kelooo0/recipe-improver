def test_register_user(client, db_session):
    response = client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "test_password"},
    )

    assert response.status_code == 201
    assert "email" in response.json()
    assert response.json()["email"] == "user@example.com"


def test_login_success(client, db_session):
    client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "test_password"},
    )
    response = client.post(
        "/auth/login",
        data={"username": "user@example.com", "password": "test_password"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "Bearer"


def test_login_wrong_password(client, db_session):
    client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "test_password"},
    )
    response = client.post(
        "/auth/login",
        data={"username": "user@example.com", "password": "test_password1"},
    )

    assert response.status_code == 401
    assert "detail" in response.json()
    assert response.json()["detail"] == "Incorrect email or password"
