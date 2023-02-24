import pytest


@pytest.mark.django_db
def test_create(authenticated_admin_client):
    reaction_data = {
        "reaction_code": "LK",
    }
    response = authenticated_admin_client.post("/reactions/", data=reaction_data, format="json")
    assert response.status_code == 201
    assert response.data["reaction_code"] == reaction_data["reaction_code"]


@pytest.mark.django_db
def test_read_all(authenticated_admin_client):
    response = authenticated_admin_client.get("/reactions/")
    assert response.status_code == 200
    assert len(response.data) > 0


@pytest.mark.django_db
def test_read_one(authenticated_admin_client):
    reaction_data = {
        "reaction_code": "LK",
    }
    response = authenticated_admin_client.post("/reactions/", data=reaction_data, format="json")
    reaction_id = response.data["id"]
    response = authenticated_admin_client.get(f"/reactions/{reaction_id}/")
    assert response.status_code == 200
    assert response.data["reaction_code"] == reaction_data["reaction_code"]


@pytest.mark.django_db
def test_update(authenticated_admin_client):
    reaction_data = {
        "reaction_code": "LK",
    }
    response = authenticated_admin_client.post("/reactions/", data=reaction_data, format="json")
    reaction_id = response.data["id"]

    updated_data = {"reaction_code": "CL", }
    response = authenticated_admin_client.put(f"/reactions/{reaction_id}/", data=updated_data, format="json")
    assert response.status_code == 200
    assert response.data["reaction_code"] == updated_data["reaction_code"]


@pytest.mark.django_db
def test_delete(authenticated_admin_client):
    reaction_data = {
        "reaction_code": "LK",
    }
    response = authenticated_admin_client.post("/reactions/", data=reaction_data, format="json")
    reaction_id = response.data["id"]

    response = authenticated_admin_client.delete(f"/reactions/{reaction_id}/")
    assert response.status_code == 204

    response = authenticated_admin_client.get(f"/reactions/{reaction_id}/")
    assert response.status_code == 404
