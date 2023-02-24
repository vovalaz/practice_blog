import pytest
from rest_framework.test import APIClient
from users import services as user_services
from reactions.models import Reaction


@pytest.fixture
def user():
    user_instance = user_services.UserDataClass(username="zewald", email="vovalaz321@gmail.com", password="zalavov687")
    user = user_services.create_user(user_instance)

    return user


@pytest.fixture
def admin_user():
    user_instance = user_services.UserDataClass(username="vovalaz", email="vovalaz@gmail.com", password="zalavov687")
    user = user_services.create_superuser(user_instance)

    return user


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def authenticated_client(user, api_client):
    response = api_client.post("/token/", {"email": user.email, "password": "zalavov687"})
    access_token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client


@pytest.fixture
def authenticated_admin_client(admin_user, api_client: APIClient):
    response = api_client.post("/token/", {"email": admin_user.email, "password": "zalavov687"})
    access_token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client


@pytest.fixture
def like_reaction():
    reaction = Reaction(reaction_code="LK")
    reaction.save()
    return reaction
