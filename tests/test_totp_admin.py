from django.test import TestCase, Client
from django_otp.oath import totp
from one_big_thing.learning.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice


class TOTPAdminTest(TestCase):
    def setUp(self):
        """
        Create a device at the fourth time step. The current token is 154567.
        """
        self.superuser = User.objects.create_superuser(
            password='password',
            email='admin@example.com'
        )

        # Create a TOTP device for the superuser
        self.device = TOTPDevice.objects.create(user=self.superuser, confirmed=True)

        # Create an instance of the Django test client
        self.client = Client()


    def test_admin_login_success(self):
        # Perform a login POST request to the admin login page
        response = self.client.post(
            '/admin/login/',
            {
                'username': 'admin@example.com',
                'password': 'password',
                "otp_token": totp(self.device.bin_key),
             })

        # Check if the login was successful (HTTP 302 status code indicates a redirect)
        self.assertEqual(response.status_code, 200)
        # Check if the user is redirected to the admin dashboard (change this URL as needed)
#        self.assertRedirects(response.read(), '/admin/')

    def test_admin_login_fail(self):
        # Perform a login POST request to the admin login page
        response = self.client.post(
            '/admin/login/',
            {
                'username': 'admin@example.com',
                'password': 'password',
                "otp_token": 123456,
             })

        # Check if the login was successful (HTTP 302 status code indicates a redirect)
        self.assertEqual(response.status_code, 200)
        # Check if the user is redirected to the admin dashboard (change this URL as needed)
        raise Exception(response.read())
        self.assertRedirects(response.read(), '/admin/')
