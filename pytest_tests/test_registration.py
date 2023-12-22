import uuid

import pytest

from one_big_thing.learning import email_handler, models


class MockUser:
    def __init__(self, email):
        self.last_token_sent_at = None
        self.last_login = None
        self.id = uuid.uuid4()
        self.email = email

    def save(self):
        pass


@pytest.mark.django_db
def test_incorrect_token(client):
    user = MockUser(email="incorrect-token@example.com")
    url = email_handler._make_token_url(user, "email-register")
    page = client.get(url)
    assert "Login failed" in page.content.decode()


@pytest.mark.django_db
def test_reused_token(client):
    email = "double-login@example.com"
    user = models.User.objects.create_user(email=email)
    assert not user.last_login
    url = email_handler._make_token_url(user, "email-register")
    page = client.get(url, follow=True)
    assert "About you" in page.content.decode()
    user = models.User.objects.get(email=email)
    assert not user.completed_personal_details
    assert user.last_login
    page = client.get(url)
    assert "Login failed" in page.content.decode()
