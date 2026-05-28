from unittest.mock import patch


@patch("app.services.searches_service.ai_service.generate_recipes")
def test_create_search(mock_ai, authorized_client, db_session):

    ai_data = [
        {"title": "string", "content": "string", "prep_time": 0},
        {"title": "string", "content": "string", "prep_time": 0},
        {"title": "string", "content": "string", "prep_time": 0},
    ]

    mock_ai.return_value = ai_data
    ingredients_list = ["string", "string", "string"]
    response = authorized_client.post(
        "/searches", params={"ingredients": ingredients_list}
    )

    assert response.status_code == 201
    search = response.json()
    assert "ingredients" in search
    assert "search_recipes" in search
    assert search["ingredients"] == "string, string, string"
    assert search["search_recipes"][0]["title"] == "string"


def test_get_searches(test_search, authorized_client, db_session):
    response = authorized_client.get("/searches")

    assert response.status_code == 200
    search = response.json()[0]
    assert "ingredients" in search
    assert "search_recipes" in search
    assert search["ingredients"] == "string, string, string"
    assert search["search_recipes"][0]["title"] == "string"
