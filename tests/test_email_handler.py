from one_big_thing.learning import models
from one_big_thing.learning.models import Department

from . import utils


def test_send_email_learning_record():
    client = utils.make_testino_client()
    email = "jim@example.com"
    page = client.get("/")
    form = page.get_form()
    form["email"] = email
    page = form.submit()
    user = models.User.objects.get(email=email)
    user.has_completed_pre_survey = True
    user.verified = True
    user.grade = "GRADE7"
    user.profession = "ANALYSIS"
    user.department = Department.objects.get(code="cabinet-office")
    user.save()
    url = utils._get_latest_email_url()
    page = client.get(url)
    page = client.get("/send-learning-record/")
    form = page.get_form()
    new_person_email = "a_different_email@example.com"
    form["email"] = new_person_email
    page = form.submit()
    assert page.has_text(f"Your learning record has successfully been sent to {new_person_email}")
    email_body = utils._get_latest_email_text()
    assert f"To: {new_person_email}" in email_body, email_body
