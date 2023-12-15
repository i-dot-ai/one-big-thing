from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.template.loader import render_to_string

from one_big_thing.learning.models import User

COMMANDS = [
    (
        User.objects.no_learning_recorded,
        "Have you recorded your learning for One Big Thing?",
        "email/recorded-your-learning.txt",
    ),
    (
        User.objects.seven_hours_no_end_evaluation,
        "Have you provided feedback on your One Big Thing experience yet?",
        "email/provide-feedback.txt",
    ),
]


class Command(BaseCommand):
    help = """gather stats on user completions, options are:
    0. no_learning_recorded
    1. seven_hours_no_end_evaluation
    """

    def add_arguments(self, parser):
        parser.add_argument("-c", "--cmd", type=str, choices=[0, 1], nargs=1, help="command to run", default=0)

    def handle(self, *args, **kwargs):
        command, subject, template = COMMANDS[kwargs["cmd"]]

        message = render_to_string(template)

        for user in command():
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.FROM_EMAIL,
                recipient_list=[user.email],
            )
