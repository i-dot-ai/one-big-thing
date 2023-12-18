import pytest

from one_big_thing.api_serializers import SurveyParticipantSerializer
from one_big_thing.learning.models import SurveyResult
from one_big_thing.learning.survey_handling import (
    awareness_level_questions_data,
    post_questions_data,
    practitioner_level_questions_data,
    pre_questions_data,
    unknown_level_questions_data,
    working_level_questions_data,
)


@pytest.mark.django_db
def test_serialize_user(create_user):
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
        data={"confident-in-decisions": "very-confident"},
        survey_type="pre",
        page_number=1,
    )

    SurveyResult.objects.create(
        user=user,
        data={"training-level": "practitioner"},
        survey_type="post",
        page_number=1,
    )
    serializer = SurveyParticipantSerializer(instance=user)

    output = serializer.to_representation(user)

    assert output["pre"]["confident-in-decisions"] == "very-confident"
    assert output["post"]["training-level"] == "practitioner"

    for k, v in output["pre"].items():
        if k != "confident-in-decisions":
            assert v == ""

    for k, v in output["post"].items():
        if k != "training-level":
            assert v == ""


@pytest.mark.django_db
def test_serialize_user_with_multiple_surveys(create_user):
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
        data={"confident-in-decisions": "very-confident"},
        survey_type="pre",
        page_number=1,
    )

    SurveyResult.objects.create(
        user=user,
        data={"help-team": "no"},
        survey_type="pre",
        page_number=1,
    )

    SurveyResult.objects.create(
        user=user,
        data={"training-level": "practitioner"},
        survey_type="post",
        page_number=1,
    )

    SurveyResult.objects.create(
        user=user,
        data={"aware-of-aims": "yes"},
        survey_type="post",
        page_number=1,
    )

    serializer = SurveyParticipantSerializer(instance=user)

    output = serializer.to_representation(user)

    assert output["pre"]["confident-in-decisions"] == "very-confident"
    assert output["pre"]["help-team"] == "no"
    assert output["post"]["training-level"] == "practitioner"
    assert output["post"]["aware-of-aims"] == "yes"


@pytest.mark.django_db
def test_serialize_user_without_surveys(create_user):
    # we don't expect this to be required in practice, but good
    # to know it won't fall over
    user = create_user(
        email="chris@co.gov.uk",
        date_joined="2000-01-02",
        grade="GRADE6",
        times_to_complete=[60],
        has_completed_pre_survey=False,
        has_completed_post_survey=False,
    )

    serializer = SurveyParticipantSerializer(instance=user)

    output = serializer.to_representation(user)

    for k, v in output["pre"].items():
        assert v == ""

    for k, v in output["post"].items():
        assert v == ""


@pytest.mark.django_db
def test_serialize_user_with_overrides(create_user):
    user = create_user(
        email="chris@co.gov.uk",
        date_joined="2000-01-02",
        grade="GRADE6",
        times_to_complete=[60],
        has_completed_pre_survey=True,
        has_completed_post_survey=True,
    )

    first = SurveyResult.objects.create(
        user=user,
        data={"help-team": "yes"},
        survey_type="pre",
        page_number=1,
    )
    second = SurveyResult.objects.create(
        user=user,
        data={"help-team": "no"},
        survey_type="pre",
        page_number=1,
    )

    assert first.created_at < second.created_at

    serializer = SurveyParticipantSerializer(instance=user)

    output = serializer.to_representation(user)

    assert output["pre"]["help-team"] == "no"


def _build_questions(survey_type, survey_sub_type, question):
    return [(survey_type, survey_sub_type, q["id"]) for d in question for q in d["questions"]]


ALL_QUESTIONS = (
    _build_questions("pre", "pre", pre_questions_data)
    + _build_questions("post", "post", post_questions_data)
    + _build_questions("post", "awareness", awareness_level_questions_data)
    + _build_questions("post", "working", working_level_questions_data)
    + _build_questions("post", "practitioner", practitioner_level_questions_data)
    + _build_questions("post", "unknown", unknown_level_questions_data)
)


@pytest.mark.parametrize("survey_type, survey_sub_type, question", ALL_QUESTIONS)
@pytest.mark.django_db
def test_serialize_user_all_question_fields(create_user, survey_type, survey_sub_type, question):
    """For each question, we create a survey result with the type (pre/post) and sub-type (other)
    and the question, and assign the answer 'yes'.
    We then asserts that the output has the question and answer are correctly assigned
    """
    user = create_user(
        email="chris@co.gov.uk",
        date_joined="2000-01-02",
        grade="GRADE6",
        times_to_complete=[60],
    )

    SurveyResult.objects.create(
        user=user,
        data={question: "yes"},
        survey_type=survey_sub_type,
        page_number=1,
    )

    serializer = SurveyParticipantSerializer(instance=user)

    output = serializer.to_representation(user)

    assert output[survey_type][question] == "yes"
