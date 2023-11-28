import random
from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from one_big_thing.learning import models
from one_big_thing.learning.models import Department
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
        department=Department.objects.get(code="acas"),
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
    record = {
        "date_joined": today_date,
        "number_of_signups": 1,
        "department": "acas",
        "parent": "DEPARTMENT_FOR_BUSINESS_AND_TRADE",
    }
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
def test_breakdown_stats(authenticated_api_client_fixture, alice, bob, chris, daisy, eric):  # noqa: F811
    url = reverse("normalized_user_statistics")
    response = authenticated_api_client_fixture.get(url)
    assert response.status_code == 200, response.status_code

    def f(grade, user_count, has_completed_pre_survey, has_completed_post_survey, bucketed_hours):
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

    expected = [
        (6, 1, True, True, "(0,1)"),  # eric
        (6, 2, True, True, "[1,2)"),  # chris & daisy
        (7, 1, False, False, "0"),  # authenticated user for the client!
        (7, 1, False, False, "[1,2)"),  # alice
        (7, 1, True, False, "[3,4)"),  # bob
    ]
    assert response.json()["results"] == [f(*x) for x in expected]


@pytest.mark.django_db
def test_breakdown_stats_page_size(authenticated_api_client_fixture, alice, bob, chris, daisy, eric):  # noqa: F811
    url = reverse("normalized_user_statistics")
    response = authenticated_api_client_fixture.get(url, {"page_size": 2})
    assert response.status_code == 200, response.status_code
    assert len(response.json()["results"]) == 2


@pytest.mark.django_db
def test_get_department_stats(authenticated_api_client_fixture, alice, bob, chris, daisy, eric):  # noqa: F811
    url = reverse("department_learning")
    response = authenticated_api_client_fixture.get(url)
    assert response.status_code == 200, response.status_code
    assert len(response.json()["results"]) == 1


@pytest.mark.django_db
def test_get_surveys(
    authenticated_api_client_fixture, alice, bob, chris, daisy, eric, pre_survey_data, post_survey_data
):  # noqa: F811
    url = reverse("surveys")
    response = authenticated_api_client_fixture.get(url)
    assert response.status_code == 200, response.status_code

    g6 = next(x for x in response.json()["results"] if x["grade"] == "GRADE6")
    g7 = next(x for x in response.json()["results"] if x["grade"] == "GRADE7")

    assert len(g6["learning_records"]) == 1
    assert len(g7["learning_records"]) == 2

    assert "pre" in g6
    assert "pre" in g7
    assert "post" not in g6
    assert "post" in g7
