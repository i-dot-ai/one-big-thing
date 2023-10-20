import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [
        "/home/",
        "/record-learning/",
        "/questions/pre/",
        "/questions/post/",
        "/complete-hours/",
        "/send-learning-record/",
        "/intro-pre-survey/",
        "/end-pre-survey/",
        "/intro-post-survey/",
        "/end-post-survey/",
        "/department-links/",
    ],
)
@pytest.mark.parametrize("login, status_code", [(True, 200), (False, 401)])
def test_get_pages_logged_in(client, alice, url, login, status_code):
    if login:
        client.force_login(alice)
    response = client.get(url, follow=True)
    assert response.status_code == status_code
