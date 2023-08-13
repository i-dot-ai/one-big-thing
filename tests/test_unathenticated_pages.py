from django.test import override_settings

from one_big_thing.learning import models

from . import utils

ACCOUNT_URLS_LOGIN_NOT_REQUIRED = [
    "/accounts/verify/",
    "/accounts/password-reset/",
    "/accounts/change-password/reset/",
    "/accounts/password-reset-done/",
    "/accounts/password-reset-from-key-done/",
    "/accounts/login/",
    "/accounts/signup/",
    "/accounts/verify/resend/",
]


@utils.with_client
def test_get_account_urls_login_not_required(client):
    for url in ACCOUNT_URLS_LOGIN_NOT_REQUIRED:
        response = client.get(url)
        assert response.status_code == 200, response.status_code


def test_login():
    client = utils.make_testino_client()
    email = "fred@example.com"
    password = "StupidPassword1!"
    page = client.get("/accounts/signup/")
    form = page.get_form()
    form["email"] = email
    form["password1"] = password
    form["password2"] = password
    form["grade"] = "GRADE6"
    form["department"] = "visitengland"
    form["profession"] = "LEGAL"
    form.submit().follow()
    page = client.get("/").follow()
    # email verification off for tests
    assert page.has_text("Thank you for registering for One Big Thing.")
    page = client.get("/accounts/login/")
    form = page.get_form()
    form["login"] = email
    form["password"] = "wrong_password"
    page = form.submit()
    assert page.has_text("Something has gone wrong.")
    form = page.get_form()
    form["login"] = email
    form["password"] = password
    form.submit()
    page = client.get("/").follow()
    assert page.has_text("Thank you for registering for One Big Thing.")
    models.User.objects.get(email=email).delete()


@override_settings(SEND_VERIFICATION_EMAIL=True)
def test_email_verification():
    client = utils.make_testino_client()
    email = "james@example.com"
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
    assert page.has_text("Sign up complete")
    assert page.has_text("verification email")
    verification_url = utils._get_latest_email_url()
    # Verification should take to homepage, which redirects to start of survey
    page = client.get(verification_url).follow()
    assert page.status_code == 302, page.status_code  # Homepage redirects
    page = page.follow()
    assert page.has_text("Thank you for registering for One Big Thing")


def test_invalid_password_requirements():
    email = "Annie4@example.com"
    # TODO - readd test that email and password aren't too similar
    # invalid_passwords = ["password1!", "elephants$5", "PinkPanda", "h12!L", email]
    invalid_passwords = ["password1!", "elephants$5", "PinkPanda", "h12!L"]
    client = utils.make_testino_client()
    for pwd in invalid_passwords:
        page = client.get("/accounts/signup/")
        form = page.get_form()
        form["email"] = email
        form["grade"] = "GRADE7"
        form["department"] = "home-office"
        form["profession"] = "ANALYSIS"
        form["password1"] = pwd
        form["password2"] = pwd
        page = form.submit()
        # ie return to registration page unable to progress
        assert page.has_text("Register"), pwd
