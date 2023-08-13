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
    client.get("/accounts/logout/")
    page = client.get("/accounts/login/")
    form = page.get_form()
    form["login"] = email
    form["password"] = "wrong_password"
    page = form.submit()
    print(page)
    assert page.has_text("Something has gone wrong.")
    form = page.get_form()
    form["login"] = email
    form["password"] = password
    form.submit()
    page = client.get("/").follow()
    assert page.has_text("Thank you for registering for One Big Thing.")
    models.User.objects.get(email=email).delete()


# def test_verification():
#     # sign-up
#     # Check page has "Sign up complete"

#     # Get verification URL
#     # Follow URL and check logged in?



# Test password requirements