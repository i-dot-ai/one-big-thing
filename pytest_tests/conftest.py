import uuid
from datetime import datetime

import pytest
import pytz
from django.urls import reverse
from rest_framework.test import APIClient

from one_big_thing.learning.models import Learning, User
from pytest_tests.utils import TEST_USER_EMAIL, TEST_USER_PASSWORD

UTC = pytz.timezone("UTC")


@pytest.fixture
def create_user():
    def _create_user(**kwargs):
        email = kwargs.pop("email", None)
        date_joined = kwargs.pop("date_joined", None)
        department = kwargs.pop("department", "acas")
        grade = kwargs.pop("grade", "GRADE7")
        profession = kwargs.pop("profession", "ANALYSIS")
        has_completed_pre_survey = kwargs.pop("has_completed_pre_survey", False)
        has_completed_post_survey = kwargs.pop("has_completed_post_survey", False)
        times_to_complete = kwargs.pop("times_to_complete", [])

        if email is None:
            email = (f"test_{uuid.uuid4()}@example.com",)

        if date_joined is None:
            date_joined = datetime.now()
        else:
            date_joined = UTC.localize(datetime.fromisoformat(date_joined))

        user = User.objects.create_user(
            email=email,
            date_joined=date_joined,
            department=department,
            grade=grade,
            profession=profession,
            has_completed_pre_survey=has_completed_pre_survey,
            has_completed_post_survey=has_completed_post_survey,
        )

        for time_to_complete in times_to_complete:
            Learning.objects.create(
                time_to_complete=time_to_complete,
                user=user,
            )

        return user

    return _create_user


@pytest.fixture
def alice(create_user):
    return create_user(
        email="alice@co.gov.uk",
        date_joined="2000-01-01",
        times_to_complete=[60],
    )


@pytest.fixture
def bob(create_user):
    return create_user(
        email="bob@co.gov.uk", date_joined="2000-01-01", times_to_complete=[60, 120], has_completed_pre_survey=True
    )


@pytest.fixture
def chris(create_user):
    return create_user(
        email="chris@co.gov.uk",
        date_joined="2000-01-02",
        grade="GRADE6",
        times_to_complete=[60],
        has_completed_pre_survey=True,
        has_completed_post_survey=True,
    )


@pytest.fixture
def api_client():
    client = APIClient()
    yield client


@pytest.fixture
def token(api_client):
    user, _ = User.objects.get_or_create(
        email=TEST_USER_EMAIL,
        is_api_user=True,
        department="acas",
        grade="GRADE7",
        profession="ANALYSIS",
    )
    user.set_password(TEST_USER_PASSWORD)
    user.save()
    url = reverse("token_obtain_pair")
    response = api_client.post(url, {"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD})
    assert response.status_code == 200, response.status_code
    assert response.data.get("access"), response.data
    token = response.data.get("access")
    return token


@pytest.fixture
def authenticated_api_client_fixture(token, api_client):
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    return api_client
