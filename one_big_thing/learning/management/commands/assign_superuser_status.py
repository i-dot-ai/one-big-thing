import getpass

from django.core.management import BaseCommand
from django_otp.plugins.otp_totp.models import TOTPDevice
from one_big_thing.learning.models import User



class Command(BaseCommand):
    help = """This should be run once per environment to set the initial superuser. 
    Thereafter the superuser should assign new staff users via the admin and send 
    them the link to the Authenticator.
    
    Once run this command will return the link to a Time-One-Time-Pass that the 
    superuser should use to enable login to the admin portal."""

    def add_arguments(self, parser):
        parser.add_argument("-e", "--email", type=str, help="user's email", required=True)

    def handle(self, *args, **kwargs):
        email = kwargs["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"User with email '{email}' does not exist."))
            return
        except User.MultipleObjectsReturned:
            self.stderr.write(self.style.ERROR(f"Multiple users found with email '{email}'."))
            return

        user.is_superuser = True
        if not user.password:
            password = getpass.getpass('Password: ')
            user.set_password(password)

        user.save()

        device, _ = TOTPDevice.objects.get_or_create(user=user, confirmed=True, tolerance=0)
        self.stdout.write(device.config_url)
        return
