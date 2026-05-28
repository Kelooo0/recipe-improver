import pytest
from app.config import settings
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch

engine = create_engine(
    settings.TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)

    connection = engine.connect()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    connection.close()

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def authorized_client(client, db_session):
    client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "test_password"},
    )
    response = client.post(
        "/auth/login",
        data={"username": "user@example.com", "password": "test_password"},
    )
    access_token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client


@pytest.fixture
def another_authorized_client(client, db_session):
    client.post(
        "/auth/register",
        json={"email": "user2@example.com", "password": "test_password"},
    )
    response = client.post(
        "/auth/login",
        data={"username": "user2@example.com", "password": "test_password"},
    )
    access_token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client


@pytest.fixture
def test_user(authorized_client, db_session):
    from app.models import UserModel

    return (
        db_session.query(UserModel)
        .filter(UserModel.email == "user@example.com")
        .first()
    )


@pytest.fixture
@patch("app.services.searches_service.ai_service.generate_recipes")
def test_search(mock_ai, test_user, db_session):
    from app.services.searches_service import create_search_service

    ai_data = [
        {"title": "string", "content": "string", "prep_time": 0},
        {"title": "string", "content": "string", "prep_time": 0},
        {"title": "string", "content": "string", "prep_time": 0},
    ]

    mock_ai.return_value = ai_data
    ingredients_list = ["string", "string", "string"]
    return create_search_service(ingredients_list, test_user, db_session)


@pytest.fixture
def test_recipe(test_user, db_session):
    from app.schemas import RecipeCreate
    from app.services.recipes_service import create_recipe_service

    recipe_data = RecipeCreate(title="string", content="string", prep_time=0)

    return create_recipe_service(recipe_data, test_user, db_session)
