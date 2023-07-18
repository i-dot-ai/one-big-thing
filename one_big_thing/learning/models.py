import logging
import uuid

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django_use_email_as_username.models import BaseUser, BaseUserManager

from one_big_thing.learning import choices, utils

logger = logging.getLogger(__name__)


class UUIDPrimaryKeyBase(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    modified_at = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        abstract = True


class User(BaseUser, UUIDPrimaryKeyBase):
    objects = BaseUserManager()
    username = None
    verified = models.BooleanField(default=False, blank=True, null=True)
    invited_at = models.DateTimeField(default=None, blank=True, null=True)
    invite_accepted_at = models.DateTimeField(default=None, blank=True, null=True)
    last_token_sent_at = models.DateTimeField(editable=False, blank=True, null=True)
    is_external_user = models.BooleanField(editable=True, default=False)
    has_marked_complete = models.BooleanField(editable=True, default=False)
    department = models.CharField(max_length=254, blank=True, null=True)
    grade = models.CharField(max_length=25, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.is_external_user = not utils.is_civil_service_email(self.email)
        super().save(*args, **kwargs)

    def has_signed_up(self):
        return self.last_login is not None

    def has_completed_required_time(self):
        completions = self.completion_set.all()
        total_time = sum([completion.course.time_to_complete for completion in completions])
        required_time = settings.REQUIRED_LEARNING_TIME
        return total_time >= required_time

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

    def get_learning_type_display_name(self):
        if self.learning_type in choices.CourseType.names:
            return choices.CourseType.mapping[self.learning_type]
        else:
            return ""


class Completion(TimeStampedModel, UUIDPrimaryKeyBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)


class Event(TimeStampedModel):
    name = models.CharField(max_length=256)
    data = models.JSONField(encoder=DjangoJSONEncoder)


class SurveyResult(UUIDPrimaryKeyBase, TimeStampedModel):
    data = models.JSONField(null=True, blank=True)
    page_number = models.IntegerField()
    survey_type = models.CharField(max_length=4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
