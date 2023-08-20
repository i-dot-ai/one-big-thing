from django.test import override_settings

from one_big_thing.learning import models

from . import utils


@override_settings(SEND_VERIFICATION_EMAIL=True)
def test_send_email_learning_record():
    client = utils.make_testino_client()
    email = "jim@example.com"
    password = "StupidPassword1!"
    page = client.get("/accounts/signup/")
    form = page.get_form()
    form["email"] = email
    form["password1"] = password
    form["password2"] = password
    form["grade"] = "GRADE7"
    form["department"] = "hm-treasury"
    form["profession"] = "LEGAL"
    page = form.submit()
    user = models.User.objects.get(email=email)
    user.has_completed_pre_survey = True
    user.verified = True
    user.save()
    page = client.get("/accounts/login/")
    form = page.get_form()
    form["login"] = email
    form["password"] = password
    form.submit()
    page = client.get("/send-learning-record/")
    form = page.get_form()
    new_person_email = "a_different_email@example.com"
    form["email"] = new_person_email
    page = form.submit()
    assert page.has_text(f"Your learning record has successfully been sent to {new_person_email}")
    email_body = utils._get_latest_email_text()
    assert f"To: {new_person_email}" in email_body, email_body
