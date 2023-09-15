from . import utils

ACCOUNT_URLS_MISSING = [
    "/accounts/verify/",
    "/accounts/password-reset/",
    "/accounts/change-password/reset/",
    "/accounts/password-reset-done/",
    "/accounts/password-reset-from-key-done/",
    "/accounts/login/",
    "/accounts/signup/",
    "/accounts/verify/resend/",
]

INFO_PAGES_LOGIN_NOT_REQUIRED = ["/privacy-notice/", "/support/", "/accessibility-statement/"]


@utils.with_client
def test_get_account_urls_not_there(client):
    for url in ACCOUNT_URLS_MISSING:
        response = client.get(url)
        assert response.status_code == 404, response.status_code


def test_login():
    client = utils.make_testino_client()
    email = "james@example.com"
    page = client.get("/")
    form = page.get_form()
    form["email"] = email
    page = form.submit().follow()
    assert page.has_text("Sign in email sent")
    verification_url = utils._get_latest_email_url()
    page = client.get(verification_url)
    # Verification should take to homepage, which redirects to "About you"
    page = page.follow().follow().follow().follow()
    assert page.has_text("About you")
