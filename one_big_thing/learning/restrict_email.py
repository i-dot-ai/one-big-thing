from django.conf import settings
from django.forms import ValidationError


def clean_email(email):
    email = email.lower()
    domain = email.split("@")[-1]
    email_allowed = domain in settings.ALLOWED_CIVIL_SERVICE_DOMAINS
    if not email_allowed:
        raise ValidationError(
            f"Currently you need a Civil Service email address to register. If you think your email address should be allowed contact us on <a href='mailto:{settings.FEEDBACK_EMAIL}'>{settings.FEEDBACK_EMAIL}</a>"
        )
    return email
