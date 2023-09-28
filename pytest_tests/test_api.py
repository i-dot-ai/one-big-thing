import random
from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from one_big_thing.learning import models
from one_big_thing.learning.api_views import get_learning_breakdown_data
from pytest_tests.utils import (  # noqa: F401
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
    add_user,
)


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
    record = {"date_joined": today_date, "number_of_signups": 1}
    dates = [item["date_joined"] for item in response.data]
    assert record in response.data, response.data
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


@pytest.mark.django_db
def test_breakdown_stats(authenticated_api_client_fixture, add_user):  # noqa: F811
    num_of_users = random.randint(0, 1200)
    for i in range(0, num_of_users):
        add_user(i)
    url = reverse("user_statistics")
    response = authenticated_api_client_fixture.get(url)
    assert response.status_code == 200, response.status_code
    selected_item = None
    for item in response.data:
        if item["department"] == "acas" and item["grade"] == "GRADE7" and item["profession"] == "ANALYSIS":
            selected_item = item
    num_user_in_data = sum([a["number_of_sign_ups"] for a in response.data])
    assert num_user_in_data == num_of_users + 1, (num_user_in_data, num_of_users)
    assert selected_item is not None, selected_item
    assert selected_item["number_of_sign_ups"] == 1, selected_item
    assert response.data, response.data


@pytest.mark.django_db
def test_breakdown_stats(alice, bob, chris, daisy, eric):  # noqa: F811
    learning_breakdown_data = list(get_learning_breakdown_data())

    assert len(learning_breakdown_data) == 2

    grade7 = next(x for x in learning_breakdown_data if x["grade"] == "GRADE7")
    assert grade7["number_of_sign_ups"] == 2  # alice and bob are grade 7
    assert grade7["completed_first_evaluation"] == 1  # alice has done no training, bob has done the first one
    assert grade7["completed_second_evaluation"] == 0
    assert (
        grade7["completed_1_hours_of_learning"] == 1
    )  # alice has done 1 course of 1 hour, bob has done 1 course of one hour and one with 2
    assert grade7["completed_2_hours_of_learning"] == 1  # only bob shows up here

    grade6 = next(x for x in learning_breakdown_data if x["grade"] == "GRADE6")
    assert grade6["number_of_sign_ups"] == 3  # chris & daisy have this grade
    assert grade6["completed_first_evaluation"] == 3  # chris has completed both evaluations
    assert grade6["completed_second_evaluation"] == 2  # 1 course, 1 hour
    assert grade6["completed_1_hours_of_learning"] == 0
    assert grade6["completed_2_hours_of_learning"] == 0
