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
    grade = models.CharField(max_length=254, blank=True, null=True)
    profession = models.CharField(max_length=254, blank=True, null=True)
    has_completed_pre_survey = models.BooleanField(default=False)
    has_completed_post_survey = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.is_external_user = not utils.is_civil_service_email(self.email)
        super().save(*args, **kwargs)

    def has_signed_up(self):
        return self.last_login is not None

    def has_completed_required_time(self):
        learnings = self.learning_set.all()
        total_time = sum([learning.time_to_complete for learning in learnings])
        required_time = settings.REQUIRED_LEARNING_TIME
        return total_time >= required_time

    def get_time_completed(self):
        learnings = self.learning_set.all()
        total_time = sum([learning.time_to_complete for learning in learnings])
        return total_time

    def has_completed_course(self, course_id):
        learnings = self.learning_set.all()
        course_ids = [learning.course_id for learning in learnings if learning.course_id]
        return course_id in course_ids


class Course(TimeStampedModel, UUIDPrimaryKeyBase):
    title = models.CharField(max_length=100)
    link = models.URLField(blank=True, null=True)
    learning_type = models.CharField(max_length=128, blank=True, null=True)
    time_to_complete = models.IntegerField()  # minutes
    # strengths = models.CharField(max_length=255)

    def get_learning_type_display_name(self):
        if self.learning_type in choices.CourseType.names:
            return choices.CourseType.mapping[self.learning_type]
        else:
            return ""


class Learning(TimeStampedModel, UUIDPrimaryKeyBase):
    title = models.CharField(max_length=100)
    link = models.URLField(blank=True, null=True)
    learning_type = models.CharField(max_length=128, blank=True, null=True)
    time_to_complete = models.IntegerField()  # minutes
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_learning_type_display_name(self):
        if self.learning_type in choices.CourseType.names:
            return choices.CourseType.mapping[self.learning_type]
        else:
            return ""


class Event(TimeStampedModel):
    name = models.CharField(max_length=256)
    data = models.JSONField(encoder=DjangoJSONEncoder)


class SurveyResult(UUIDPrimaryKeyBase, TimeStampedModel):
    data = models.JSONField(null=True, blank=True)
    page_number = models.IntegerField()
    survey_type = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
