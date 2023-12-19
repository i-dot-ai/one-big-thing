import uuid
from datetime import date, datetime

import pytest
import pytz
from django.core.management import call_command

from one_big_thing.learning.models import (
    Department,
    Learning,
    SurveyResult,
    User,
)

UTC = pytz.timezone("UTC")


@pytest.fixture(autouse=True, scope="session")
def collect_static():
    call_command("collectstatic", "--noinput")


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
def pre_survey_data():
    return {
        "confident-in-decisions": "very-confident",
        "confidence-graphic-survey": "not-confident",
        "confidence-explaining-chart": "confident",
        "confident-day-to-day": "",
        "data-support-day-to-day": "",
        "data-is-relevant-to-role": "2",
        "use-data-effectively-day-to-day": "",
        "line-manager": "",
        "help-team": "",
        "coach-team": "",
        "support-team": "",
        "training-last-six-months": "",
        "training-analytical-component": "yes",
        "aware-of-the-aims": "4",
        "shared-identity": "3",
        "identity-is-important": "2",
        "willing-to-follow-up": "yes",
    }


@pytest.fixture
def post_survey_data():
    return {
        "training-level": "practitioner",
        "shared-identity": "4",
        "identity-important": "4",
        "confident-day-to-day": "4",
        "data-support-day-to-day": "",
        "data-is-relevant-to-role": "",
        "use-data-effectively-day-to-day": "",
        "line-manager": "no",
        "help-team": "",
        "coach-team": "",
        "support-team": "",
        "anticipate-data-limitations": "",
        "understanding-ethics-for-data": "",
        "understand-how-to-quality-assure-data": "",
        "more-effectively-communicate-data-insights-to-improve-decisions": "",
        "find-mentor": "",
        "book-training": "",
        "other-development": "",
        "create-development-plan": "",
        "add-learning-to-development-plan": "5",
        "training-helped-learning": "",
        "conversations-helped-learning": "",
        "additional-resources-helped-learning": "",
        "useful-learning-formats": "",
        "obt-good-use-of-time": "",
        "content-was-relevant-to-my-role": "",
        "intend-to-apply-learning-in-my-role": "4",
        "improved-understanding-of-using-data": "",
        "intend-to-participate-in-further-training": "",
        "aware-of-aims": "",
        "sufficient-time": "",
        "what-went-well": "",
        "what-can-be-improved": "",
        "willing-to-follow-up": "no",
    }


@pytest.fixture
def alice(create_user):
    user = create_user(
        email="alice@co.gov.uk",
        date_joined="2000-01-01",
        grade="GRADE7",
        times_to_complete=[60],
        has_completed_pre_survey=False,
        has_completed_post_survey=False,
    )
    return user


@pytest.fixture
def bob(create_user, pre_survey_data, post_survey_data):
    user = create_user(
        email="bob@co.gov.uk",
        date_joined="2000-01-01",
        grade="GRADE7",
        times_to_complete=[60, 120],
        has_completed_pre_survey=True,
        has_completed_post_survey=False,
    )
    SurveyResult.objects.create(
        user=user,
        data=pre_survey_data,
        survey_type="pre",
        page_number=1,
    )
    SurveyResult.objects.create(
        user=user,
        data=post_survey_data,
        survey_type="post",
        page_number=1,
    )
    return bob


@pytest.fixture
def chris(create_user, pre_survey_data):
    user = create_user(
        email="chris@co.gov.uk",
        date_joined="2000-01-02",
        grade="GRADE6",
        times_to_complete=[60],
        has_completed_pre_survey=True,
        has_completed_post_survey=True,
    )

    SurveyResult.objects.create(
        user=user,
        data=pre_survey_data,
        survey_type="pre",
        page_number=1,
    )
    return user


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
