from django.conf import settings
from django.forms import ValidationError

from one_big_thing.learning import utils


def clean_email(email):
    email_allowed = utils.is_civil_service_email(email)
    email = email.lower()
    if not email_allowed:
        raise ValidationError(
            f"Currently you need a Civil Service email address to register. If you think your email address should be allowed contact us on <a href='mailto:{settings.FEEDBACK_EMAIL}'>{settings.FEEDBACK_EMAIL}</a>"  # noqa: E501
        )
    return email
