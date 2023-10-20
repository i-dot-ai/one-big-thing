import pytest
from django_otp.oath import totp
from django_otp.plugins.otp_totp.models import TOTPDevice

from one_big_thing.learning.models import User


@pytest.fixture
def otp_token():
    superuser = User.objects.create_superuser(password="password", email="admin@example.com")

    # Create a TOTP device for the superuser
    device = TOTPDevice.objects.create(user=superuser, confirmed=True)

    yield totp(device.bin_key)


@pytest.mark.django_db
def test_admin_login_success(client, otp_token):
    # Perform a login POST request to the admin login page
    response = client.post(
        "/admin/login/",
        {
            "username": "admin@example.com",
            "password": "password",
            "otp_token": otp_token,
            "next": "/admin/",
        },
    )

    # Check if the login was successful (HTTP 302 status code indicates a redirect)
    assert response.status_code == 302
    # Check if the user is redirected to the admin dashboard
    assert response["Location"] == "/admin/"


@pytest.mark.django_db
def test_admin_login_fail(client, otp_token):
    # Perform a login POST request to the admin login page
    response = client.post(
        "/admin/login/",
        {
            "username": "admin@example.com",
            "password": "password",
            "otp_token": 123456,
        },
    )

    # Check if the login was unsuccessful (bizarrely this is an HTTP 200 status code)
    assert response.status_code == 200
    # check that the correct error is returned
    assert "Invalid token. Please make sure you have entered it correctly." in str(response.content)
