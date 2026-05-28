def test_create_recipe(authorized_client, db_session):
    response = authorized_client.post(
        "/recipes", json={"title": "string", "content": "string", "prep_time": 0}
    )

    assert response.status_code == 201
    recipe = response.json()
    assert "title" in recipe
    assert "content" in recipe
    assert "prep_time" in recipe
    assert recipe["title"] == "string"
    assert recipe["content"] == "string"
    assert recipe["prep_time"] == 0


def test_get_recipes(test_recipe, authorized_client, db_session):
    response = authorized_client.get("/recipes")

    assert response.status_code == 200
    recipe = response.json()[0]
    assert "title" in recipe
    assert "content" in recipe
    assert recipe["title"] == "string"
    assert recipe["content"] == "string"
    assert recipe["prep_time"] == 0


def test_get_recipe(test_recipe, authorized_client, db_session):
    response = authorized_client.get(f"/recipes/{test_recipe.id}")

    assert response.status_code == 200
    recipe = response.json()
    assert "title" in recipe
    assert "content" in recipe
    assert recipe["title"] == "string"
    assert recipe["content"] == "string"
    assert recipe["prep_time"] == 0


def test_update_recipe(test_recipe, authorized_client, db_session):
    response = authorized_client.patch(
        f"/recipes/{test_recipe.id}",
        json={"title": "another_string", "content": "another_string", "prep_time": 5},
    )

    assert response.status_code == 200
    recipe = response.json()
    assert "title" in recipe
    assert "content" in recipe
    assert recipe["title"] == "another_string"
    assert recipe["content"] == "another_string"
    assert recipe["prep_time"] == 5


def test_delete_recipe(test_recipe, authorized_client, db_session):
    response = authorized_client.delete(f"/recipes/{test_recipe.id}")

    assert response.status_code == 204
    from app.models import RecipeModel

    recipe_model = (
        db_session.query(RecipeModel).filter(RecipeModel.id == test_recipe.id).first()
    )
    assert recipe_model is None


def test_cannot_view_other_users_recipe(
    test_recipe, authorized_client, another_authorized_client, db_session
):
    response = another_authorized_client.get(f"/recipes/{test_recipe.id}")

    assert response.status_code == 404
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Recipe not found"
