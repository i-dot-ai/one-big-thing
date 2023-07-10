import datetime

import furl as furl
import pytz
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.template.loader import render_to_string

from one_big_thing.learning import models


def _strip_microseconds(dt):
    if not dt:
        return None
    return dt.replace(microsecond=0, tzinfo=None)


class EmailVerifyTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        email = user.email or ""
        token_timestamp = _strip_microseconds(user.last_token_sent_at)
        return f"{user.pk}{user.password}{timestamp}{email}{token_timestamp}"


class PasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        login_timestamp = _strip_microseconds(user.last_login)
        email = user.email or ""
        token_timestamp = _strip_microseconds(user.last_token_sent_at)
        return f"{user.pk}{user.password}{login_timestamp}{timestamp}{email}{token_timestamp}"


class InviteTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        invited_timestamp = _strip_microseconds(user.invited_at)
        email = user.email or ""
        token_timestamp = _strip_microseconds(user.last_token_sent_at)
        return f"{user.pk}{invited_timestamp}{timestamp}{email}{token_timestamp}"


EMAIL_VERIFY_TOKEN_GENERATOR = EmailVerifyTokenGenerator()
PASSWORD_RESET_TOKEN_GENERATOR = PasswordResetTokenGenerator()
INVITE_TOKEN_GENERATOR = InviteTokenGenerator()


EMAIL_MAPPING = {
    "email-verification": {
        "from_address": settings.FROM_EMAIL,
        "subject": "Evaluation Registry: confirm your email address",
        "template_name": "email/verification.txt",
        "url_path": "/accounts/verify/",
        "token_generator": EMAIL_VERIFY_TOKEN_GENERATOR,
    },
    "password-reset": {
        "from_address": settings.FROM_EMAIL,
        "subject": "Evaluation Registry: password reset",
        "template_name": "email/password-reset.txt",
        "url_path": "/accounts/change-password/reset/",
        "token_generator": PASSWORD_RESET_TOKEN_GENERATOR,
    },
    "add-contributor": {
        "from_address": settings.FROM_EMAIL,
        "subject": "Evaluation Registry: invited to contribute",
        "template_name": "email/invite-to-evaluation.txt",
    },
    "invite-user": {
        "from_address": settings.FROM_EMAIL,
        "subject": "Evaluation Registry: invited to join",
        "template_name": "email/invite-user.txt",
        "url_path": "/accounts/accept-invite/",
        "token_generator": INVITE_TOKEN_GENERATOR,
    },
    "account-already-exists": {
        "from_address": settings.FROM_EMAIL,
        "subject": "Evaluation Registry: registration attempt",
        "template_name": "email/account-already-exists.txt",
        "url_path": "/accounts/password-reset/",
    },
}


def _send_token_email(user, subject, template_name, from_address, url_path, token_generator):
    user.last_token_sent_at = datetime.datetime.now(tz=pytz.UTC)
    user.save()
    token = token_generator.make_token(user)
    base_url = settings.BASE_URL
    url = str(furl.furl(url=base_url, path=url_path, query_params={"code": token, "user_id": str(user.id)}))
    context = dict(user=user, url=url, contact_address=settings.CONTACT_EMAIL)
    body = render_to_string(template_name, context)
    response = send_mail(
        subject=subject,
        message=body,
        from_email=from_address,
        recipient_list=[user.email],
    )
    return response


def _send_normal_email(subject, template_name, from_address, to_address, context):
    body = render_to_string(template_name, context)
    response = send_mail(
        subject=subject,
        message=body,
        from_email=from_address,
        recipient_list=[to_address],
    )
    return response


def send_verification_email(user):
    data = EMAIL_MAPPING["email-verification"]
    return _send_token_email(user, **data)


def send_password_reset_email(user):
    data = EMAIL_MAPPING["password-reset"]
    return _send_token_email(user, **data)


def send_invite_email(user):
    data = EMAIL_MAPPING["invite-user"]
    user.invited_at = datetime.datetime.now()
    user.save()
    return _send_token_email(user, **data)


def send_contributor_added_email(user, evaluation_id):
    data = EMAIL_MAPPING["add-contributor"]
    base_url = settings.BASE_URL
    url = furl.furl(url=base_url)
    url.path.add(f"evaluation/{evaluation_id}")
    url = str(url)
    context = {"url": url}
    response = _send_normal_email(to_address=user.email, context=context, **data)
    return response


def send_account_already_exists_email(user):
    data = EMAIL_MAPPING["account-already-exists"]
    base_url = settings.BASE_URL
    reset_url = furl.furl(url=base_url)
    reset_url.path.add(data["url_path"])
    reset_url = str(reset_url)
    context = {"contact_address": settings.CONTACT_EMAIL, "url": base_url, "reset_link": reset_url}
    response = _send_normal_email(
        subject=data["subject"],
        template_name=data["template_name"],
        from_address=data["from_address"],
        to_address=user.email,
        context=context,
    )
    return response


def verify_token(user_id, token, token_type):
    user = models.User.objects.get(id=user_id)
    result = EMAIL_MAPPING[token_type]["token_generator"].check_token(user, token)
    return result
