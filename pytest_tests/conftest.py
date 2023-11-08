import uuid
from datetime import date, datetime

import pytest
import pytz

from one_big_thing.learning.models import Department, Learning, User

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
            department=Department.objects.get(code=department),
            grade=grade,
            profession=profession,
            has_completed_pre_survey=has_completed_pre_survey,
            has_completed_post_survey=has_completed_post_survey,
        )

        for i, time_to_complete in enumerate(times_to_complete):
            Learning.objects.create(time_to_complete=time_to_complete, user=user, created_at=date(2020 + i, 11, 8))

        return user

    return _create_user


@pytest.fixture
def alice(create_user):
    return create_user(
        email="alice@co.gov.uk",
        date_joined="2000-01-01",
        grade="GRADE7",
        times_to_complete=[60],
        has_completed_pre_survey=False,
        has_completed_post_survey=False,
    )


@pytest.fixture
def bob(create_user):
    return create_user(
        email="bob@co.gov.uk",
        date_joined="2000-01-01",
        grade="GRADE7",
        times_to_complete=[60, 120],
        has_completed_pre_survey=True,
        has_completed_post_survey=False,
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
def daisy(create_user):
    return create_user(
        email="daisy@co.gov.uk",
        date_joined="2000-01-02",
        grade="GRADE6",
        times_to_complete=[30, 60],
        has_completed_pre_survey=True,
        has_completed_post_survey=True,
    )


@pytest.fixture
def eric(create_user):
    return create_user(
        email="eric@co.gov.uk",
        date_joined="2000-01-02",
        times_to_complete=[5, 10],
        department="active-travel-england",
        grade="GRADE6",
        has_completed_pre_survey=True,
        has_completed_post_survey=True,
    )


@pytest.fixture
def faye(create_user):
    return create_user(
        email="faye@co.gov.uk",
        date_joined="2000-01-02",
        times_to_complete=[0, 0],
        grade="GRADE6",
        has_completed_pre_survey=True,
        has_completed_post_survey=True,
    )


@pytest.fixture
def george(create_user):
    return create_user(
        email="george@co.gov.uk",
        date_joined="2000-01-02",
        grade="GRADE6",
        has_completed_pre_survey=True,
        has_completed_post_survey=True,
    )


@pytest.fixture
def hannah(create_user):
    return create_user(
        email="hannah@co.gov.uk",
        date_joined="2000-01-02",
        grade="GRADE6",
        times_to_complete=[60, 120, 240, 480],
        has_completed_pre_survey=True,
        has_completed_post_survey=True,
    )


@pytest.fixture
def isaac(create_user):
    return create_user(
        email="isaac@co.gov.uk",
        date_joined="2000-01-02",
        grade="GRADE6",
        times_to_complete=[60, 120, 240, 480, 6000000],
        has_completed_pre_survey=True,
        has_completed_post_survey=False,
    )
