import pytest


@pytest.mark.django_db
def test_create(authenticated_client):
    post_data = {
        "title": "Random text",
        "text_content": "Random content"
    }
    response = authenticated_client.post("/posts/", data=post_data, format="json")
    assert response.status_code == 201
    assert response.data["title"] == post_data["title"]
    assert response.data["text_content"] == post_data["text_content"]


@pytest.mark.django_db
def test_read_all(api_client):
    response = api_client.get("/posts/")
    assert response.status_code == 200
    assert len(response.data) > 0


@pytest.mark.django_db
def test_read_one(authenticated_client):
    post_data = {
        "title": "Random text",
        "text_content": "Random content"
    }
    response = authenticated_client.post("/posts/", data=post_data, format="json")
    post_id = response.data["id"]
    response = authenticated_client.get(f"/posts/{post_id}/")
    assert response.status_code == 200
    assert response.data["title"] == post_data["title"]


@pytest.mark.django_db
def test_update(authenticated_client):
    post_data = {
        "title": "Random text",
        "text_content": "Random content"
    }
    response = authenticated_client.post("/posts/", data=post_data, format="json")
    post_id = response.data["id"]

    updated_data = {"title": "Updated Title", "text_content": "Updated content"}
    response = authenticated_client.put(f"/posts/{post_id}/", data=updated_data, format="json")
    assert response.status_code == 200
    assert response.data["title"] == updated_data["title"]


@pytest.mark.django_db
def test_delete(authenticated_client):
    post_data = {
        "title": "Random text",
        "text_content": "Random content"
    }
    response = authenticated_client.post("/posts/", data=post_data, format="json")
    post_id = response.data["id"]

    response = authenticated_client.delete(f"/posts/{post_id}/")
    assert response.status_code == 204

    response = authenticated_client.get(f"/posts/{post_id}/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_react_to_post(authenticated_client, like_reaction):
    post_data = {
        "title": "Random text",
        "text_content": "Random content"
    }
    response = authenticated_client.post("/posts/", data=post_data, format="json")
    post_id = response.data["id"]
    reaction_data = {
        "reaction": "LK",
    }
    response = authenticated_client.post(f"/posts/{post_id}/reaction/", data=reaction_data, format="json")

    assert response.status_code == 201
    assert response.data["reaction"] == reaction_data["reaction"]
    assert response.data["post"]
    assert response.data["status"] == "saved"

    response = authenticated_client.post(f"/posts/{post_id}/reaction/", data=reaction_data, format="json")
    assert response.status_code == 204
    assert response.data["status"] == "deleted"
