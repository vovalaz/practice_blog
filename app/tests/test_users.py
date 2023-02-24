import pytest


@pytest.mark.django_db
def test_register_user(api_client):
    user_data = {
        "username": "zewald",
        "email": "vovalaz321@gmail.com",
        "password": "zalavov236",
    }
    response = api_client.post("/users/", user_data)
    data = response.data

    assert response.status_code == 201, "status code after registering a new user was not 201"
    assert data["username"] == user_data["username"], "returned username don't match one from user_data"
    assert data["email"] == user_data["email"], "returned email don't match one from user_data"
    assert "password" not in data, "password is not supposed to be returned"


@pytest.mark.django_db
def test_login_user(user, api_client):
    response = api_client.post("/token/", {"email": "vovalaz321@gmail.com", "password": "zalavov687"})
    data = response.data
    assert response.status_code == 200, "login was not successful"
    assert data["refresh"], "refresh token was not found in response"
    assert data["access"], "access token was not found in response"


@pytest.mark.django_db
def test_login_user_failed(api_client):
    response = api_client.post("/token/", {"email": "not_valid_email@abc.com", "password": "ababagalamaga"})
    assert response.status_code == 401, "invalid login didn't return unauthorised"


@pytest.mark.django_db
def test_list(api_client):
    response = api_client.get("/users/")
    assert response.status_code == 200, "status code on list was not 200"
    assert len(response.data) > 0, "response data was empty"


@pytest.mark.django_db
def test_retrieve(api_client):
    user_data = {
        "username": "zewald",
        "email": "vovalaz321@gmail.com",
        "password": "zalavov236",
    }
    response = api_client.post("/users/", user_data, format="json")
    user_id = response.data["id"]

    response = api_client.get(f"/users/{user_id}/")
    assert response.status_code == 200, "status code on retrieve was not 200"
    assert response.data["username"] == user_data["username"], "response username don't match setted username"
    assert response.data["email"] == user_data["email"], "response email don't match setted email"


@pytest.mark.django_db
def test_partial_update(authenticated_admin_client):
    user_data = {
        "username": "zewald",
        "email": "vovalaz321@gmail.com",
        "password": "zalavov236",
    }
    response = authenticated_admin_client.post("/users/", data=user_data, format="json")
    user_id = response.data["id"]

    updated_data = {"username": "new_user"}
    response = authenticated_admin_client.patch(f"/users/{user_id}/", data=updated_data, format="json")
    assert response.status_code == 200, f"status code on partial update was not 200 {response.data}"
    assert (
        response.data["username"] == updated_data["username"]
    ), "response username don't match partial updated data username"


@pytest.mark.django_db
def test_update(authenticated_admin_client):
    user_data = {
        "username": "zewald",
        "email": "vovalaz321@gmail.com",
        "password": "zalavov236",
    }
    response = authenticated_admin_client.post("/users/", data=user_data, format="json")
    user_id = response.data["id"]

    updated_data = {"username": "new_user", "email": "vovalazar@gmail.com"}
    response = authenticated_admin_client.put(f"/users/{user_id}/", data=updated_data, format="json")
    assert response.status_code == 200, f"status code on update was not 200 ({response.status_code})"
    assert response.data["username"] == updated_data["username"], "response username don't match updated data username"
    assert response.data["email"] == updated_data["email"], "response email don't match updated data email"


@pytest.mark.django_db
def test_delete(authenticated_admin_client):
    user_data = {
        "username": "zewald",
        "email": "vovalaz321@gmail.com",
        "password": "zalavov236",
    }
    response = authenticated_admin_client.post("/users/", data=user_data, format="json")
    user_id = response.data["id"]

    response = authenticated_admin_client.delete(f"/users/{user_id}/")
    assert response.status_code == 204, "status code after delete was not 204"

    response = authenticated_admin_client.get(f"/users/{user_id}/")
    assert response.status_code == 404, "status code after getting deleted item was not 404"
