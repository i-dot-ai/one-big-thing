from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.management import BaseCommand

from one_big_thing.learning.models import User

COMMANDS = [User.objects.no_learning_recorded, User.objects.seven_hours_no_end_evaluation]


class Command(BaseCommand):
    help = """gather stats on user completions, options are:
    0. no_learning_recorded
    1. seven_hours_no_end_evaluation
    """

    def add_arguments(self, parser):
        parser.add_argument("-e", "--email", type=str, nargs=1, help="email to send results to")
        parser.add_argument("-c", "--cmd", type=str, choices=[0, 1], nargs=1, help="command to run", default=0)

    def handle(self, *args, **kwargs):
        email = kwargs["email"]
        try:
            User.objects.get(email=email, is_staff=True)
        except ObjectDoesNotExist:
            self.stderr.write(self.style.ERROR(f"'{email}' does not exist, or is not staff"))
            return

        command = COMMANDS[kwargs["cmd"]]

        message = "\n".join(user.email for user in command())

        send_mail(
            subject=self.help, message=message, from_email=settings.FROM_EMAIL, recipient_list=[email],
        )
