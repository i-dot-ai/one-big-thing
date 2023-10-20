import logging
import uuid
from collections import Counter

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import Sum
from django_cte import CTEManager
from django_use_email_as_username.models import BaseUser, BaseUserManager

from one_big_thing.learning import choices, constants
from one_big_thing.learning.choices import Grade, Profession
from one_big_thing.learning.departments import department_tuples

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


class UserManager(BaseUserManager, CTEManager):
    """https://dimagi.github.io/django-cte/
    we need to do some complex queries on this model
    """

    pass


class User(BaseUser, UUIDPrimaryKeyBase):
    objects = UserManager()
    username = None
    verified = models.BooleanField(default=False, blank=True, null=True)
    invited_at = models.DateTimeField(default=None, blank=True, null=True)
    invite_accepted_at = models.DateTimeField(default=None, blank=True, null=True)
    last_token_sent_at = models.DateTimeField(editable=False, blank=True, null=True)
    department = models.CharField(max_length=254, blank=True, null=True, choices=department_tuples)
    grade = models.CharField(max_length=254, blank=True, null=True, choices=Grade.choices)
    profession = models.CharField(max_length=254, blank=True, null=True, choices=Profession.choices)
    has_completed_pre_survey = models.BooleanField(default=False)
    has_completed_post_survey = models.BooleanField(default=False)
    is_api_user = models.BooleanField(default=False, null=True, blank=True)

    @property
    def completed_personal_details(self) -> bool:
        return self.department and self.grade and self.profession

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    def has_signed_up(self) -> bool:
        return self.last_login is not None

    def has_completed_required_time(self) -> bool:
        total_time = self.get_time_completed()
        required_time = settings.REQUIRED_LEARNING_TIME
        return total_time >= required_time

    def get_time_completed(self) -> int:
        learning = self.learning_set.aggregate(total=Sum("time_to_complete"))
        return learning["total"] or 0

    def has_completed_course(self, course_id: int) -> bool:
        return self.learning_set.filter(course_id=course_id).exists()

    def determine_competency_level(self):
        level = None
        if self.has_completed_pre_survey:
            competency_answers = self.get_competency_answers_for_user()
            level = determine_competency_levels(competency_answers)
        return level

    def get_competency_answers_for_user(self):
        pre_survey_results = (
            SurveyResult.objects.filter(user=self).filter(survey_type="pre").values_list("data", flat=True)
        )
        pre_survey_results = {k: v for result in pre_survey_results for k, v in result.items()}
        competency_answers = [
            v for k, v in pre_survey_results.items() if k in constants.INITIAL_COMPETENCY_DETERMINATION_QUESTIONS
        ]
        return competency_answers

    class Meta:
        indexes = [
            models.Index(
                fields=("department", "grade", "profession", "has_completed_pre_survey", "has_completed_post_survey")
            )
        ]


class Course(TimeStampedModel, UUIDPrimaryKeyBase):
    title = models.CharField(max_length=200)
    link = models.URLField(blank=True, null=True)
    learning_type = models.CharField(max_length=128, blank=True, null=True, choices=choices.CourseType.choices)
    time_to_complete = models.IntegerField(blank=True, null=True)  # minutes

    def get_learning_type_display_name(self):
        if self.learning_type in choices.CourseType.names:
            return choices.CourseType.mapping[self.learning_type]
        else:
            return ""

    def __str__(self):
        return f"{self.title} ({self.id})"


class Learning(TimeStampedModel, UUIDPrimaryKeyBase):
    title = models.CharField(max_length=200)
    link = models.URLField(blank=True, null=True)
    learning_type = models.CharField(max_length=128, blank=True, null=True, choices=choices.CourseType.choices)
    time_to_complete = models.IntegerField()  # minutes
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True, null=True)

    def get_learning_type_display_name(self):
        if self.learning_type in choices.CourseType.names:
            return choices.CourseType.mapping[self.learning_type]
        else:
            return ""

    def __str__(self):
        return f"{self.title} ({self.id})"


class Event(TimeStampedModel):
    name = models.CharField(max_length=256)
    data = models.JSONField(encoder=DjangoJSONEncoder)


class SurveyResult(UUIDPrimaryKeyBase, TimeStampedModel):
    PRE = "pre"
    POST = "post"
    SURVEY_TYPE = [(PRE, "pre"), (POST, "post")]

    data = models.JSONField(null=True, blank=True)
    page_number = models.IntegerField()
    survey_type = models.CharField(max_length=128, choices=SURVEY_TYPE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.survey_type} - {self.id} - {self.modified_at}"


def determine_competency_levels(competency_answers_list):
    """
    3 competency levels, "awareness", "working", "practitioner".
    Corresponding to "not-confident",
    Take the most common to be the assigned competency level.
    In case of tie - take "working".
    """
    competency_levels_list = [
        constants.COMPETENCY_DETERMINATION_MAPPING[k] for k in competency_answers_list if k
    ]  # Also gets rid of empties
    competency_level_counts = Counter(competency_levels_list)
    if not competency_level_counts:
        return None
    max_value = max(competency_level_counts.values())
    competency_levels_most_common = [key for key, value in competency_level_counts.items() if value == max_value]
    if len(competency_levels_most_common) == 1:
        return competency_levels_most_common[0]
    else:
        return constants.WORKING
