import logging
import uuid
from collections import Counter
from typing import Any

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import Q, Sum
from django_cte import CTEManager
from django_use_email_as_username.models import BaseUser, BaseUserManager

from one_big_thing.learning import choices, constants
from one_big_thing.learning.choices import Grade, Profession
from one_big_thing.learning.constants import SURVEY_TYPES

logger = logging.getLogger(__name__)

POST_SURVEY_TYPES = [key for key, value in SURVEY_TYPES.items() if value == "post"]
PRE_SURVEY_TYPES = [key for key, value in SURVEY_TYPES.items() if value == "pre"]


class UUIDPrimaryKeyBase(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    modified_at = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        abstract = True


class Department(TimeStampedModel):
    ATTORNEY_GENERALS_DEPARTMENTS = "ATTORNEY_GENERALS_DEPARTMENTS"
    CABINET_OFFICE = "CABINET_OFFICE"
    CHANCELLORS_OTHER_DEPARTMENTS = "CHANCELLORS_OTHER_DEPARTMENTS"
    CHARITY_COMMISSION = "CHARITY_COMMISSION"
    COMPETITION_AND_MARKETS_AUTHORITY = "COMPETITION_AND_MARKETS_AUTHORITY"
    CROWN_PROSECUTION_SERVICE = "CROWN_PROSECUTION_SERVICE"
    DEPARTMENT_FOR_BUSINESS_AND_TRADE = "DEPARTMENT_FOR_BUSINESS_AND_TRADE"
    DEPARTMENT_FOR_CULTURE_MEDIA_AND_SPORT = "DEPARTMENT_FOR_CULTURE_MEDIA_AND_SPORT"
    DEPARTMENT_FOR_EDUCATION = "DEPARTMENT_FOR_EDUCATION"
    DEPARTMENT_FOR_ENERGY_SECURITY_AND_NET_ZERO = "DEPARTMENT_FOR_ENERGY_SECURITY_AND_NET_ZERO"
    DEPARTMENT_FOR_ENVIRONMENT_FOOD_AND_RURAL_AFFAIRS = "DEPARTMENT_FOR_ENVIRONMENT_FOOD_AND_RURAL_AFFAIRS"
    DEPARTMENT_FOR_LEVELLING_UP_HOUSING_AND_COMMUNITIES = "DEPARTMENT_FOR_LEVELLING_UP_HOUSING_AND_COMMUNITIES"
    DEPARTMENT_FOR_SCIENCE_INNOVATION_AND_TECHNOLOGY = "DEPARTMENT_FOR_SCIENCE_INNOVATION_AND_TECHNOLOGY"
    DEPARTMENT_FOR_TRANSPORT = "DEPARTMENT_FOR_TRANSPORT"
    DEPARTMENT_FOR_WORK_AND_PENSIONS = "DEPARTMENT_FOR_WORK_AND_PENSIONS"
    DEPARTMENT_OF_HEALTH_AND_SOCIAL_CARE = "DEPARTMENT_OF_HEALTH_AND_SOCIAL_CARE"
    FOOD_STANDARDS_AGENCY = "FOOD_STANDARDS_AGENCY"
    FOREIGN_COMMONWEALTH_AND_DEVELOPMENT_OFFICE = "FOREIGN_COMMONWEALTH_AND_DEVELOPMENT_OFFICE"
    HM_LAND_REGISTRY = "HM_LAND_REGISTRY"
    HM_REVENUE_AND_CUSTOMS = "HM_REVENUE_AND_CUSTOMS"
    HM_TREASURY = "HM_TREASURY"
    HOME_OFFICE = "HOME_OFFICE"
    MINISTRY_OF_DEFENCE = "MINISTRY_OF_DEFENCE"
    MINISTRY_OF_JUSTICE = "MINISTRY_OF_JUSTICE"
    NATIONAL_CRIME_AGENCY = "NATIONAL_CRIME_AGENCY"
    NORTHERN_IRELAND_OFFICE = "NORTHERN_IRELAND_OFFICE"
    NORTHERN_IRELAND_EXECUTIVE = "NORTHERN_IRELAND_EXECUTIVE"
    OFFICE_OF_THE_SECRETARY_OF_STATE_FOR_WALES = "OFFICE_OF_THE_SECRETARY_OF_STATE_FOR_WALES"
    OFFICE_OF_THE_SECRETARY_OF_STATE_FOR_SCOTLAND = "OFFICE_OF_THE_SECRETARY_OF_STATE_FOR_SCOTLAND"
    OFGEM = "OFGEM"
    OFQUAL = "OFQUAL"
    OTHER = "OTHER"
    OFSTED = "OFSTED"
    OFFICE_OF_RAIL_AND_ROAD = "OFFICE_OF_RAIL_AND_ROAD"
    SCOTTISH_GOVERNMENT = "SCOTTISH_GOVERNMENT"
    SUPREME_COURT_OF_THE_UNITED_KINGDOM = "SUPREME_COURT_OF_THE_UNITED_KINGDOM"
    THE_NATIONAL_ARCHIVES = "THE_NATIONAL_ARCHIVES"
    UK_EXPORT_FINANCE = "UK_EXPORT_FINANCE"
    UK_STATISTICS_AUTHORITY = "UK_STATISTICS_AUTHORITY"
    WATER_SERVICES_REGULATION_AUTHORITY = "WATER_SERVICES_REGULATION_AUTHORITY"
    WELSH_GOVERNMENT = "WELSH_GOVERNMENT"

    PARENTS = [
        (ATTORNEY_GENERALS_DEPARTMENTS, "Attorney General's Departments"),
        (CABINET_OFFICE, "Cabinet Office"),
        (CHANCELLORS_OTHER_DEPARTMENTS, "Chancellor's other departments"),
        (CHARITY_COMMISSION, "Charity Commission"),
        (COMPETITION_AND_MARKETS_AUTHORITY, "Competition and Markets Authority"),
        (CROWN_PROSECUTION_SERVICE, "Crown Prosecution Service"),
        (DEPARTMENT_FOR_BUSINESS_AND_TRADE, "Department for Business and Trade"),
        (DEPARTMENT_FOR_CULTURE_MEDIA_AND_SPORT, "Department for Culture, Media & Sport"),
        (DEPARTMENT_FOR_EDUCATION, "Department for Education"),
        (DEPARTMENT_FOR_ENERGY_SECURITY_AND_NET_ZERO, "Department for Energy Security & Net Zero"),
        (DEPARTMENT_FOR_ENVIRONMENT_FOOD_AND_RURAL_AFFAIRS, "Department for Environment Food & Rural Affairs"),
        (DEPARTMENT_FOR_LEVELLING_UP_HOUSING_AND_COMMUNITIES, "Department for Levelling Up, Housing and Communities"),
        (DEPARTMENT_FOR_SCIENCE_INNOVATION_AND_TECHNOLOGY, "Department for Science, Innovation & Technology"),
        (DEPARTMENT_FOR_TRANSPORT, "Department for Transport"),
        (DEPARTMENT_FOR_WORK_AND_PENSIONS, "Department for Work & Pensions"),
        (DEPARTMENT_OF_HEALTH_AND_SOCIAL_CARE, "Department of Health & Social Care"),
        (FOOD_STANDARDS_AGENCY, "Food Standards Agency"),
        (FOREIGN_COMMONWEALTH_AND_DEVELOPMENT_OFFICE, "Foreign, Commonwealth & Development Office"),
        (HM_LAND_REGISTRY, "HM Land Registry"),
        (HM_REVENUE_AND_CUSTOMS, "HM Revenue & Customs"),
        (HM_TREASURY, "HM Treasury"),
        (HOME_OFFICE, "Home Office"),
        (MINISTRY_OF_DEFENCE, "Ministry of Defence"),
        (MINISTRY_OF_JUSTICE, "Ministry of Justice"),
        (NATIONAL_CRIME_AGENCY, "National Crime Agency"),
        (NORTHERN_IRELAND_EXECUTIVE, "Northern Ireland Executive"),
        (NORTHERN_IRELAND_OFFICE, "Northern Ireland Office"),
        (OFFICE_OF_THE_SECRETARY_OF_STATE_FOR_WALES, "Office of the Secretary of State for Wales"),
        (OFFICE_OF_THE_SECRETARY_OF_STATE_FOR_SCOTLAND, "Office of the Secretary of State for Scotland"),
        (OFGEM, "Ofgem"),
        (OFQUAL, "Ofqual"),
        (OTHER, "Other"),
        (OFSTED, "Ofsted"),
        (OFFICE_OF_RAIL_AND_ROAD, "Office of Rail and Road"),
        (SCOTTISH_GOVERNMENT, "Scottish Government"),
        (SUPREME_COURT_OF_THE_UNITED_KINGDOM, "Supreme Court of the United Kingdom"),
        (THE_NATIONAL_ARCHIVES, "The National Archives"),
        (UK_EXPORT_FINANCE, "UK Export Finance"),
        (UK_STATISTICS_AUTHORITY, "UK Statistics Authority"),
        (WATER_SERVICES_REGULATION_AUTHORITY, "Water Services Regulation Authority"),
        (WELSH_GOVERNMENT, "Welsh Government"),
    ]

    code = models.SlugField(max_length=128, unique=True, help_text="unique code for department")
    display = models.CharField(max_length=128, help_text="display name")
    parent = models.CharField(max_length=128, choices=PARENTS, help_text="parent department")
    intranet_url = models.URLField(null=True, blank=True, help_text="intranet link")
    gov_id = models.SlugField(
        max_length=128,
        null=True,
        blank=True,
        help_text="for use in the uk gov api https://www.gov.uk/api/organisations/id",
    )

    @classmethod
    def choices(cls) -> list[tuple[Any, Any]]:
        return [(x.code, x.display) for x in cls.objects.all()]

    def __str__(self):
        return self.display


class UserManager(BaseUserManager, CTEManager):
    """https://dimagi.github.io/django-cte/
    we need to do some complex queries on this model
    """

    def no_learning_recorded(self):
        """all that have register but not recorded hours"""
        user_learning = self.annotate(total_learning=Sum("learning__time_to_complete")).order_by("email")

        zero_learning_on_some_courses = Q(total_learning=0)
        zero_learning_on_no_courses = Q(total_learning__isnull=True)

        return user_learning.filter(zero_learning_on_no_courses | zero_learning_on_some_courses)

    def seven_hours_no_end_evaluation(self):
        """all that have done 7 hours but not the end evaluation"""
        user_learning = self.annotate(total_learning=Sum("learning__time_to_complete")).order_by("email")

        seven_or_more_hours = user_learning.filter(total_learning__gte=7 * 60)
        return seven_or_more_hours.filter(has_completed_post_survey=False)


class User(BaseUser, UUIDPrimaryKeyBase):
    objects = UserManager()
    username = None
    verified = models.BooleanField(default=False, blank=True, null=True)
    invited_at = models.DateTimeField(default=None, blank=True, null=True)
    invite_accepted_at = models.DateTimeField(default=None, blank=True, null=True)
    last_token_sent_at = models.DateTimeField(editable=False, blank=True, null=True)
    old_department = models.CharField(max_length=254, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    grade = models.CharField(max_length=254, blank=True, null=True, choices=Grade.choices)
    profession = models.CharField(max_length=254, blank=True, null=True, choices=Profession.choices)
    has_completed_pre_survey = models.BooleanField(default=False)
    has_completed_post_survey = models.BooleanField(default=False)
    is_api_user = models.BooleanField(default=False, null=True, blank=True)

    @property
    def pre_survey_results(self):
        return self.surveyresult_set.filter(survey_type__in=PRE_SURVEY_TYPES).order_by("created_at")

    @property
    def post_survey_results(self):
        return self.surveyresult_set.filter(survey_type__in=POST_SURVEY_TYPES).order_by("created_at")

    @property
    def email_domain(self) -> str:
        return self.email.split("@")[-1]

    @property
    def completed_personal_details(self):
        return self.department and self.grade and self.profession

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
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

    def determine_competency_level(self):
        level = None
        if self.has_completed_pre_survey:
            competency_answers = get_competency_answers_for_user(self)
            level = determine_competency_levels(competency_answers)
        return level

    class Meta:
        indexes = [
            models.Index(
                fields=("department", "grade", "profession", "has_completed_pre_survey", "has_completed_post_survey")
            )
        ]


class Course(TimeStampedModel, UUIDPrimaryKeyBase):
    title = models.CharField(max_length=200)
    link = models.URLField(blank=True, null=True)
    learning_type = models.CharField(max_length=128, blank=True, null=True)
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
    learning_type = models.CharField(max_length=128, blank=True, null=True)
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
    data = models.JSONField(null=True, blank=True)
    page_number = models.IntegerField()
    survey_type = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.survey_type} - {self.id} - {self.modified_at}"


class Feedback(TimeStampedModel, UUIDPrimaryKeyBase):
    satisfaction = models.CharField(max_length=254, blank=True, null=True, choices=choices.Satisfaction.choices)
    improve_the_service = models.CharField(null=True, blank=True, max_length=2048)
    take_part_in_user_research = models.CharField(max_length=3, blank=False, null=False, choices=choices.YesNo.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


def get_competency_answers_for_user(user):
    pre_survey_results = SurveyResult.objects.filter(user=user).filter(survey_type="pre").values_list("data", flat=True)
    pre_survey_results = {k: v for result in pre_survey_results for k, v in result.items()}
    competency_answers = [
        v for k, v in pre_survey_results.items() if k in constants.INITIAL_COMPETENCY_DETERMINATION_QUESTIONS
    ]
    return competency_answers


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
