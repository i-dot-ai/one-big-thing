import pytest


@pytest.mark.parametrize("url",[
    "/accounts/verify/",
    "/accounts/password-reset/",
    "/accounts/change-password/reset/",
    "/accounts/password-reset-done/",
    "/accounts/password-reset-from-key-done/",
    "/accounts/login/",
    "/accounts/signup/",
    "/accounts/verify/resend/",
])
def test_get_account_urls_not_there(client, url):
    response = client.get(url)
    assert response.status_code == 404, response.status_code


@pytest.mark.django_db
def test_login(client, mailoutbox):
    email = "james@example.com"
    login_page = client.post("/", {"email": email}, follow=True)
    assert login_page.status_code == 200
    assert "Sign in email sent" in login_page.content.decode()

    verification_url = mailoutbox[-1].body.split("\n")[3]
    magic_link_page = client.get(verification_url, follow=True)
    assert magic_link_page.status_code == 200
    # Verification should take to homepage, which redirects to "About you"
    assert "About you" in magic_link_page.content.decode()
