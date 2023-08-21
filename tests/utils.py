import functools
import os
import pathlib

import httpx
import testino
from django.conf import settings

from one_big_thing import wsgi
from one_big_thing.learning.models import SurveyResult, User
from tests import test_survey

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
    test_survey.complete_survey(client, user)
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
