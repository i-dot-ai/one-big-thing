from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
from django_otp.plugins.otp_totp.models import TOTPDevice

from one_big_thing.learning.models import User


class Command(BaseCommand):
    help = """This should be run once per environment 
    to set the initial superuser, thereafter the superuser should 
    assign specific staff users and send them the link to the Authenticator"""

    def add_arguments(self, parser):
        parser.add_argument("-e", "--email", type=str, help="user's new ")
        parser.add_argument("-p", "--pwd", type=str, help="user's new password")

    def handle(self, *args, **kwargs):
        email = kwargs["email"]

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            self.stdout.write(f"user {email} does not exist")
            return

        user.is_superuser = True
        if not user.password:
            if pwd := kwargs.get("pwd"):
                user.set_password(pwd)
            else:
                self.stdout.write("user currently has no password set, pls specify it with --pwd")
                return

        user.save()

        device, _ = TOTPDevice.objects.get_or_create(user=user, confirmed=True, tolerance=0)

        self.stdout.write(device.config_url)
