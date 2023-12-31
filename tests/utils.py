import functools
import os
import pathlib

import httpx
import testino
from django.conf import settings

from one_big_thing import wsgi
from one_big_thing.learning import email_handler
from one_big_thing.learning.models import SurveyResult, User

TEST_SERVER_URL = "http://obt-server:8055/"


def with_client(func):
    @functools.wraps(func)
    def _inner(*args, **kwargs):
        with httpx.Client(app=wsgi.application, base_url=TEST_SERVER_URL) as client:
            return func(client, *args, **kwargs)

    return _inner


def with_authenticated_client(func):
    @functools.wraps(func)
    def _inner(*args, **kwargs):
        user, _ = User.objects.get_or_create(email="peter.rabbit@example.com")
        user.has_completed_pre_survey = True
        user.verified = True
        user.save()
        SurveyResult.objects.get_or_create(
            user=user,
            survey_type="pre",
            page_number=1,
            data={
                "competency": "awareness",
            },
        )
        with httpx.Client(app=wsgi.application, base_url=TEST_SERVER_URL, follow_redirects=True) as client:
            url = email_handler._make_token_url(user, "email-verification")
            client.get(url)
            return func(client, *args, **kwargs)

    return _inner


def make_testino_client():
    client = testino.WSGIAgent(wsgi.application, TEST_SERVER_URL)
    return client


def register(client, email, password, pre_survey=True):
    page = client.get("/")
    form = page.get_form()
    form["email"] = email
    form.submit().follow()
    url = _get_latest_email_url()
    response = client.get(url)
    assert response.status_code == 302
    complete_about_you(client)
    user = User.objects.get(email=email)
    if pre_survey:
        complete_pre_survey(client, user)
        page = client.get("/").follow()
        assert page.has_text("Overview - One Big Thing - GOV.UK")


def _get_latest_email_text():
    email_dir = pathlib.Path(settings.EMAIL_FILE_PATH)
    latest_email_path = max(email_dir.iterdir(), key=os.path.getmtime)
    content = latest_email_path.read_text()
    return content


def _get_latest_email_url():
    text = _get_latest_email_text()
    lines = text.splitlines()
    url_lines = tuple(word for line in lines for word in line.split() if word.startswith(TEST_SERVER_URL))
    assert len(url_lines) == 1
    email_url = url_lines[0].strip()
    whole_url = email_url.strip(",")
    url = f"/{whole_url.split(TEST_SERVER_URL)[-1]}".replace("?", "?")
    return url


def complete_about_you(client):
    # homepage should redirect to pre-survey which redirects to about me (if not completed)
    page = client.get("/").follow().follow().follow()
    assert page.has_text("About you")
    form = page.get_form()
    form["profession"] = "DIGITAL_DATA_AND_TECHNOLOGY"
    form["grade"] = "EXECUTIVE_OFFICER"
    form["department"] = "cabinet-office"
    next_page = form.submit().follow()
    return next_page


def complete_pre_survey(client, user, competency_level_answers=["confident", "not-confident", "not-confident"]):
    data = (
        (
            "How would you feel about making a decision based on information you're presented with? This might be numerical data like statistics or non-numerical data like user feedback.",  # noqa: E501
            {
                "confident-in-decisions": competency_level_answers[0],
            },
        ),
        (
            "How would you feel about designing a graphic to communicate the results of a survey? This could be an infographic, chart or other visualisation.",  # noqa: E501
            {
                "confidence-graphic-survey": competency_level_answers[1],
            },
        ),
        (
            "How would you feel about explaining to someone in your team what a chart of performance data is showing?",  # noqa: E501
            {
                "confidence-explaining-chart": competency_level_answers[2],
            },
        ),
        (
            "To what extent do you agree or disagree with the following statements?",
            {
                "confident-day-to-day": 1,
                "data-is-relevant-to-role": 1,
                "use-data-effectively-day-to-day": 5,
                "data-support-day-to-day": 1,
            },
        ),
        (
            "Are you currently a line manager?",
            {
                "line-manager": "yes",
            },
        ),
        (
            "to what extent do you agree or disagree",
            {"help-team": "1", "support-team": "2"},
        ),
        (
            "In the last 6 months, have you done any type of training?",
            {
                "training-last-six-months": "yes",
                "training-analytical-component": "yes",
            },
        ),
        (
            "To what extent do you agree or disagree with the following statement?",
            {
                "aware-of-the-aims": 1,
            },
        ),
        (
            "To what extent do you agree or disagree with the following statements?",
            {
                "shared-identity": 2,
                "identity-is-important": 1,
            },
        ),
    )

    page = client.get("/questions/pre/")

    for item in data:
        page = step_survey_page(page, *item)

    assert page.has_text("Survey completed")
    assert page.has_text("You can now start your One Big Thing learning.")
    completed_surveys = SurveyResult.objects.filter(user=user, survey_type="pre")
    assert len(completed_surveys) > 0, completed_surveys
    competency_data = completed_surveys.get(page_number=1)
    assert competency_data.data == {"confident-in-decisions": competency_level_answers[0]}, competency_data.data

    question_data = completed_surveys.get(page_number=2)
    assert question_data.data == {
        "confidence-graphic-survey": competency_level_answers[1],
    }, question_data

    question_data = completed_surveys.get(page_number=3)
    assert question_data.data == {"confidence-explaining-chart": competency_level_answers[2]}, question_data.data
    assert question_data.survey_type == "pre", question_data.survey_type

    question_data = completed_surveys.get(page_number=4)
    assert question_data.data == {
        "confident-day-to-day": "1",
        "data-is-relevant-to-role": "1",
        "use-data-effectively-day-to-day": "5",
        "data-support-day-to-day": "1",
    }, question_data.data

    question_data = completed_surveys.get(page_number=5)
    assert question_data.data == {"line-manager": "yes"}, question_data.data

    question_data = completed_surveys.get(page_number=6)
    assert question_data.survey_type == "pre", question_data.survey_type
    assert question_data.data == {
        "help-team": "1",
        "support-team": "2",
        "coach-team": "",
    }, question_data.data

    question_data = completed_surveys.get(page_number=7)
    assert question_data.data == {
        "training-last-six-months": "yes",
        "training-analytical-component": "yes",
    }, question_data.data

    question_data = completed_surveys.get(page_number=8)
    assert question_data.data == {"aware-of-the-aims": "1"}, question_data.data

    question_data = completed_surveys.get(page_number=9)
    assert question_data.data == {"shared-identity": "2", "identity-is-important": "1"}, question_data.data


def step_survey_page(page, title, fields):
    assert page.status_code == 200, page.status_code
    assert page.has_text(title), title
    form = page.get_form()
    for field in fields:
        form[field] = fields[field]
    next_page = form.submit().follow()
    return next_page


def complete_post_survey_awareness(client, user):
    data = (
        (
            "Which level of training did you participate in?",
            {
                "training-level": "awareness",
            },
        ),
        (
            "Please rate how much you agree or disagree with the following statements:",
            {"shared-identity": "2", "identity-important": "4"},
        ),
        (
            "I feel confident about using data in my day-to-day role",
            {
                "confident-day-to-day": "2",
                "data-is-relevant-to-role": "4",
                "use-data-effectively-day-to-day": "1",
                "data-support-day-to-day": "2",
            },
        ),
        (
            "Are you currently a line manager?",
            {"line-manager": "yes"},
        ),
        (
            'If you answered "Yes" to the previous question please answer the following. Otherwise move on to the next page. To what extent do you agree or disagree with the following statements',  # noqa: E501
            {
                "help-team": "3",
                "support-team": "1",
            },
        ),
        (
            "I have a better understanding of what data means",
            {
                "i-understand-what-data-means": "1",
                "better-at-interpreting-data": "3",
                "interested-in-working-with-data-in-day-to-day": "4",
                "more-confident-using-data-for-decisions": "3",
                "more-confident-communicating-data-to-influence-decisions": "3",
            },
        ),
        (
            "Following One Big Thing",
            {
                "create-development-plan": "1",
                "add-learning-to-development-plan": "3",
                "book-training": "4",
                "find-mentor": "3",
                "other-development": "Doing loads more learning",
            },
        ),
        (
            "Please rate how much you agree or disagree",
            {
                "training-helped-learning": "1",
                "additional-resources-helped-learning": "5",
            },
        ),
        (
            "Were there any formats of additional training you found useful?",
            {"useful-learning-formats": ["VIDEO"]},
        ),
        (
            "Please rate how much you agree or disagree",
            {
                "obt-good-use-of-time": "1",
                "improved-understanding-of-using-data": "3",
                "intend-to-participate-in-further-training": "3",
                "intend-to-apply-learning-in-my-role": "5",
            },
        ),
        (
            "Please rate how much you agree or disagree",
            {
                "aware-of-aims": "1",
                "sufficient-time": "2",
            },
        ),
        (
            "Further questions",
            {
                "what-went-well": "I found out loads of cool stuff about data.",
                "what-can-be-improved": "Even more things to learn.",
            },
        ),
        (
            "Would you be willing to take part in a follow-up discussion?",
            {"willing-to-follow-up": "yes"},
        ),
    )

    page = client.get("/questions/post/")

    for item in data:
        page = step_survey_page(page, *item)

    assert page.has_text("Thank you")

    question_data = SurveyResult.objects.get(user=user, page_number=1, survey_type="post")
    assert question_data.data == {"training-level": "awareness"}, question_data.data
    question_data = SurveyResult.objects.get(user=user, page_number=2, survey_type="post")
    assert question_data.data == {"shared-identity": "2", "identity-important": "4"}, question_data.data

    question_data = SurveyResult.objects.get(user=user, page_number=2, survey_type="awareness")
    assert question_data.data == {
        "create-development-plan": "1",
        "add-learning-to-development-plan": "3",
        "book-training": "4",
        "find-mentor": "3",
        "other-development": "Doing loads more learning",
    }, question_data.data
    question_data = SurveyResult.objects.get(user=user, page_number=3, survey_type="awareness")
    assert question_data.data == {
        "training-helped-learning": "1",
        "conversations-helped-learning": "",
        "additional-resources-helped-learning": "5",
    }, question_data.data
    question_data = SurveyResult.objects.get(user=user, page_number=4, survey_type="awareness")
    assert question_data.data == {"useful-learning-formats": ["VIDEO"]}, question_data.data
    question_data = SurveyResult.objects.get(user=user, page_number=7, survey_type="awareness")
    assert question_data.data == {
        "what-went-well": "I found out loads of cool stuff about data.",
        "what-can-be-improved": "Even more things to learn.",
    }, question_data.data
