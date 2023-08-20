import functools
import os
import pathlib

import httpx
import testino
from django.conf import settings

from one_big_thing import wsgi
from one_big_thing.learning.models import SurveyResult, User

TEST_SERVER_URL = "http://one-big-thing-testserver:8055/"


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
        user.set_password("P455W0rd!£")
        user.has_completed_pre_survey = True
        user.save()
        SurveyResult.objects.get_or_create(
            user=user,
            survey_type="pre",
            page_number=1,
            data={
                "competency": "beginner",
            },
        )
        with httpx.Client(app=wsgi.application, base_url=TEST_SERVER_URL, follow_redirects=True) as client:
            response = client.get("/accounts/login/")
            csrf = response.cookies["csrftoken"]
            data = {"login": user.email, "password": "P455W0rd!£"}
            headers = {"X-CSRFToken": csrf}
            client.post("/accounts/login/", data=data, headers=headers)
            return func(client, *args, **kwargs)

    return _inner


def make_testino_client():
    client = testino.WSGIAgent(wsgi.application, TEST_SERVER_URL)
    return client


def register(client, email, password):
    page = client.get("/accounts/signup/")
    form = page.get_form()
    form["email"] = email
    form["password1"] = password
    form["password2"] = password
    form["grade"] = "GRADE6"
    form["department"] = "visitengland"
    form["profession"] = "LEGAL"
    form.submit().follow()
    user = User.objects.get(email=email)
    complete_survey(client, user)
    page = client.get("/").follow()
    assert page.has_text("One Big Thing home")


def _get_latest_email_text():
    email_dir = pathlib.Path(settings.EMAIL_FILE_PATH)
    latest_email_path = max(email_dir.iterdir(), key=os.path.getmtime)
    content = latest_email_path.read_text()
    return content


def _get_latest_email_url():
    text = _get_latest_email_text()
    lines = text.splitlines()
    url_lines = tuple(word for line in lines for word in line.split() if word.startswith("http://localhost:8055/"))
    assert len(url_lines) == 1
    email_url = url_lines[0].strip()
    whole_url = email_url.strip(",")
    url = f"/{whole_url.split('http://localhost:8055/')[-1]}".replace("?", "?")
    return url


def complete_survey(client, user, competency_level_answers=["confident", "not-confident", "not-confident"]):
    first_page = client.get("/questions/pre/")
    second_page = step_survey_page(
        first_page,
        "How would you feel about making a decision based on information you're presented with? This might be numerical data like statistics or non-numerical data like user feedback.",  # noqa: E501
        {
            "confident-in-decisions": competency_level_answers[0],
        },
    )
    third_page = step_survey_page(
        second_page,
        "How would you feel about designing a graphic to communicate the results of a survey? This could be an infographic, chart or other visualisation.", # noqa: E501
        {
            "confidence-graphic-survey": competency_level_answers[1],
        },
    )
    fourth_page = step_survey_page(
        third_page,
        "How would you feel about explaining to someone in your team what a chart of performance data is showing?", # noqa: E501
        {
            "confidence-explaining-chart": competency_level_answers[2],
        },
    )
    fifth_page = step_survey_page(
        fourth_page,
        "To what extent do you agree or disagree with the following statement?",
        {
            "aware-of-the-aims": 1,
        },
    )
    sixth_page = step_survey_page(
        fifth_page,
        "To what extent do you agree or disagree with the following statements?",
        {
            "shared-identity": 2,
            "identity-is-important": 1,
        },
    )
    seventh_page = step_survey_page(
        sixth_page,
        "To what extent do you agree or disagree with the following statements?",
        {
            "confident-day-to-day": 1,
            "data-is-relevant-to-role": 1,
            "use-data-effectively-day-to-day": 5,
            "data-support-day-to-day": 1,
        },
    )
    eighth_page = step_survey_page(
        seventh_page,
        "Are you currently a line manager?",
        {
            "line-manager": "yes",
        },
    )
    ninth_page = step_survey_page(
        eighth_page,
        'If you answered "yes" to the previous question, to what extent do you agree or disagree with the following statements?', # noqa: E501
        {"help-team": "yes", "support-team": "dont-know", "coach-team": "no"},
    )
    tenth_page = step_survey_page(
        ninth_page,
        "In the last 6 months, have you done any type of training?",
        {
            "training-last-six-months": "yes",
        },
    )
    completed_page = step_survey_page(
        tenth_page,
        'If you answered "yes" to the previous question, did it have an analytical component (eg data, evaluation)', # noqa: E501
        {
            "training-analytical-component": "yes",
        },
    )

    assert completed_page.has_text("Survey completed")
    assert completed_page.has_text("You can now start your One Big Thing learning.")

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


def step_survey_page(page, title, fields):
    assert page.status_code == 200, page.status_code
    assert page.has_text(title), title
    form = page.get_form("""form:not([action])""")
    for field in fields:
        form[field] = fields[field]
    next_page = form.submit().follow()
    return next_page
