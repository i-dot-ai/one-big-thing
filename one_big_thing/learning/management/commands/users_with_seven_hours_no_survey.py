from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.template.loader import render_to_string

from one_big_thing.learning.models import User


class Command(BaseCommand):
    help = "nudge users who have completed seven hours to complete their feedback"

    def handle(self, *args, **kwargs):
        message = render_to_string("email/provide-feedback.txt")

        for user in User.objects.seven_hours_no_end_evaluation():
            send_mail(
                subject="Have you provided feedback on your One Big Thing experience yet?",
                message=message,
                from_email=settings.FROM_EMAIL,
                recipient_list=[user.email],
            )
