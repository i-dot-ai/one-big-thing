from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from one_big_thing.learning import models

TEST_USER_EMAIL = "test_api@example.com"
TEST_USER_PASSWORD = "test-api-password"


@pytest.fixture
def token_fixture():
    user, _ = models.User.objects.get_or_create(
        email=TEST_USER_EMAIL,
        is_api_user=True,
        department="acas",
        grade="GRADE7",
        profession="ANALYSIS",
    )
    user.set_password(TEST_USER_PASSWORD)
    user.save()
    client = APIClient()
    url = reverse("token_obtain_pair")
    response = client.post(url, {"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD})
    assert response.status_code == 200, response.status_code
    assert response.data.get("access"), response.data
    token = response.data.get("access")
    return token


@pytest.fixture
def authenticated_api_client_fixture(token_fixture):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token_fixture)
    return client


@pytest.mark.django_db
def test_get_token_user_does_not_exist():
    client = APIClient()
    url = reverse("token_obtain_pair")
    response = client.post(url, {"email": "no-user@example.com", "password": "nothingburger"})
    assert response.status_code == 401, response.status_code


@pytest.mark.django_db
def test_get_token_user_does_not_have_access():
    email = "test_api_no_access@example.com"
    password = "test-api-password"
    user, _ = models.User.objects.get_or_create(email=email, is_api_user=False)
    user.set_password(password)
    user.save()
    client = APIClient()
    url = reverse("token_obtain_pair")
    response = client.post(url, {"email": email, "password": password})
    assert response.status_code == 401, response.status_code


@pytest.mark.django_db
def test_get_signup_data(authenticated_api_client_fixture):
    url = reverse("signup_statistics")
    response = authenticated_api_client_fixture.get(url)
    assert response.status_code == 200, response.status_code
    today_date = datetime.today().date().strftime("%Y-%m-%d")
    dates = [item["date_joined"] for item in response.data]
    assert today_date in dates, dates
    assert response.data, response.data


@pytest.mark.django_db
def test_get_signup_date_failure():
    client = APIClient()
    url = reverse("signup_statistics")
    response = client.get(url)
    assert response.status_code == 401, response.status_code


@pytest.mark.django_db
def test_get_data_breakdown(authenticated_api_client_fixture):
    url = reverse("user_statistics")
    response = authenticated_api_client_fixture.get(url)
    assert response.status_code == 200, response.status_code
    selected_item = None
    for item in response.data:
        if item["department"] == "acas" and item["grade"] == "GRADE7" and item["profession"] == "ANALYSIS":
            selected_item = item
    assert selected_item is not None, selected_item
    assert selected_item["number_of_sign_ups"] == 1, selected_item
    assert response.data, response.data


@pytest.mark.django_db
def test_get_data_breakdown_failure():
    client = APIClient()
    url = reverse("user_statistics")
    response = client.get(url)
    assert response.status_code == 401, response.status_code
