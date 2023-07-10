import logging
import uuid

import pyotp
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django_use_email_as_username.models import BaseUser, BaseUserManager

from one_big_thing.learning import utils

logger = logging.getLogger(__name__)


class UUIDPrimaryKeyBase(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    modified_at = models.DateTimeField(editable=False, auto_now=True)
    last_token_sent_at = models.DateTimeField(editable=False, blank=True, null=True)
    invited_at = models.DateTimeField(default=None, blank=True, null=True)
    invite_accepted_at = models.DateTimeField(default=None, blank=True, null=True)
    totp_key = models.CharField(max_length=255, blank=True, null=True)
    last_otp = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ["created_at"]

    def get_totp_uri(self):
        secret = self.get_totp_secret()
        uri = pyotp.utils.build_uri(
            secret=secret,
            name=self.email,
            issuer=settings.TOTP_ISSUER,
        )
        return uri

    def get_totp_secret(self):
        if not self.totp_key:
            self.totp_key = utils.make_totp_key()
            self.save()
        totp_secret = utils.make_totp_secret(self.id, self.totp_key)
        return totp_secret

    def verify_otp(self, otp):
        if otp == self.last_otp:
            logger.error("OTP same as previous one")
            return False
        secret = self.get_totp_secret()
        totp = pyotp.TOTP(secret)
        success = totp.verify(otp)
        if success:
            self.last_otp = otp
            self.save()
        return success


class User(BaseUser, UUIDPrimaryKeyBase):
    objects = BaseUserManager()
    username = None

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    def get_time_completed(self):
        completions = self.completion_set.all()
        total_time = sum([completion.course.time_to_complete for completion in completions])
        return total_time


class Course(TimeStampedModel, UUIDPrimaryKeyBase):
    title = models.CharField(max_length=100)
    link = models.URLField(blank=True, null=True)
    learning_type = models.CharField(max_length=5, blank=True, null=True)
    time_to_complete = models.IntegerField()
    # strengths = models.CharField(max_length=255)


class Completion(TimeStampedModel, UUIDPrimaryKeyBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)


class Event(TimeStampedModel):
    name = models.CharField(max_length=256)
    data = models.JSONField(encoder=DjangoJSONEncoder)
