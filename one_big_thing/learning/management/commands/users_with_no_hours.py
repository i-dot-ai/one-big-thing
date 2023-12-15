from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.template.loader import render_to_string

from one_big_thing.learning.models import User


class Command(BaseCommand):
    help = "nudege users who have completed no training"

    def handle(self, *args, **kwargs):
        message = render_to_string("email/recorded-your-learning.txt")

        for user in User.objects.no_learning_recorded():
            send_mail(
                subject="Have you recorded your learning for One Big Thing?",
                message=message,
                from_email=settings.FROM_EMAIL,
                recipient_list=[user.email],
            )
