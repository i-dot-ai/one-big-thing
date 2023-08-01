from . import utils

OTHER_URLS_LOGIN_NOT_REQUIRED = ["/"]
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

# TODO - all auth urls?
# TODO - should we need login for some of these views?


@utils.with_client
def test_get_account_urls_login_not_required(client):
    for url in ACCOUNT_URLS_LOGIN_NOT_REQUIRED:
        response = client.get(url)
        assert response.status_code == 200, response.status_code
