from django.test import Client, TestCase
from django_otp.oath import totp
from django_otp.plugins.otp_totp.models import TOTPDevice

from one_big_thing.learning.models import User


class TOTPAdminTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(password="password", email="admin@example.com")

        # Create a TOTP device for the superuser
        self.device = TOTPDevice.objects.create(user=self.superuser, confirmed=True)

        # Create an instance of the Django test client
        self.client = Client()

    def test_admin_login_success(self):
        # Perform a login POST request to the admin login page
        response = self.client.post(
            "/admin/login/",
            {
                "username": "admin@example.com",
                "password": "password",
                "otp_token": totp(self.device.bin_key),
                "next": "/admin/",
            },
        )

        # Check if the login was successful (HTTP 302 status code indicates a redirect)
        self.assertEqual(response.status_code, 302)
        # Check if the user is redirected to the admin dashboard
        self.assertRedirects(response, "/admin/")

    def test_admin_login_fail(self):
        # Perform a login POST request to the admin login page
        response = self.client.post(
            "/admin/login/",
            {
                "username": "admin@example.com",
                "password": "password",
                "otp_token": 123456,
            },
        )

        # Check if the login was unsuccessful (bizarrely this is an HTTP 302 status code)
        self.assertEqual(response.status_code, 200)
        # check that the correct error is returned
        self.assertContains(response, "Invalid token. Please make sure you have entered it correctly.")
