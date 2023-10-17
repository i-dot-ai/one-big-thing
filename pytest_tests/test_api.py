import random
from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from one_big_thing.learning import models
from pytest_tests.utils import (  # noqa: F401
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
    add_user,
)


@pytest.fixture
def authenticated_api_client_fixture(client_for_user):
    user, _ = models.User.objects.get_or_create(
        email=TEST_USER_EMAIL,
        is_api_user=True,
        department="acas",
        grade="GRADE7",
        profession="ANALYSIS",
    )
    client = client_for_user(user, TEST_USER_PASSWORD)
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


def make_response(grade, user_count, has_completed_pre_survey, has_completed_post_survey, bucketed_hours):
    r = {
        "department": "acas",
        "grade": f"GRADE{grade}",
        "profession": "ANALYSIS",
        "user_count": user_count,
        "has_completed_pre_survey": has_completed_pre_survey,
        "has_completed_post_survey": has_completed_post_survey,
        "bucketed_hours": bucketed_hours,
    }
    return r


@pytest.mark.django_db
def test_breakdown_stats_no10(client_for_user, alice, bob, chris, daisy, eric):
    """alice works for number 10, she should see everything"""
    client = client_for_user(alice, "password")
    url = reverse("normalized_user_statistics")
    response = client.get(url)
    assert response.status_code == 200, response.status_code

    expected = [
        (6, 1, True, True, "(0,1)"),  # eric
        (6, 2, True, True, "[1,2)"),  # chris & daisy
        (7, 1, False, False, "[1,2)"),  # alice
        (7, 1, True, False, "[3,4)"),  # bob
    ]
    assert response.json()["results"] == [make_response(*x) for x in expected]


@pytest.mark.django_db
def test_breakdown_stats_dwp(client_for_user, alice, bob, chris, daisy, eric):
    """bob and chris have dwp email addresses, bob should only be able to see dwp stats"""
    client = client_for_user(bob, "password")
    url = reverse("normalized_user_statistics")
    response = client.get(url)
    assert response.status_code == 200, response.status_code

    expected = [
        (6, 1, True, True, "[1,2)"),  # chris
        (7, 1, True, False, "[3,4)"),  # bob
    ]
    assert response.json()["results"] == [make_response(*x) for x in expected]


@pytest.mark.django_db
def test_breakdown_stats_fco(client_for_user, alice, bob, chris, daisy, eric):
    """daisy has a fco email addresses, she cant see anything"""
    client = client_for_user(daisy, "password")
    url = reverse("normalized_user_statistics")
    response = client.get(url)
    assert response.status_code == 403, response.status_code
