import functools

import httpx
import testino

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
        user.set_password("P455W0rd")
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
            data = {"login": user.email, "password": "P455W0rd"}
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
    page = form.submit().follow().follow()
    assert page.has_text("How well do you understand data topics?")
    form = page.get_form()
    form["competency"] = "intermediate"
    form.submit().follow()
    user = User.objects.get(email=email)
    user.has_completed_pre_survey = True
    user.save()
    page = client.get("/").follow()
    assert page.has_text("Welcome to your One Big Thing Learning Record")
