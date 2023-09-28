from collections import defaultdict

from django.db.models import Count, DateField, IntegerField, Q, Sum, When, Case, Value, BooleanField
from django.db.models.functions import Cast, Coalesce, TruncDate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from one_big_thing.api_serializers import (
    DateJoinedSerializer,
    DepartmentBreakdownSerializer,
    JwtTokenObtainPairSerializer,
)
from one_big_thing.learning import models
from one_big_thing.learning.api_permissions import IsAPIUser


class UserSignupStatsView(APIView):
    """
    Endpoint used by 10DS to get information about user signups per date
    """

    permission_classes = (
        IsAuthenticated,
        IsAPIUser,
    )

    def get(self, request):
        signups = get_signups_by_date()
        serializer = DateJoinedSerializer(
            signups,
            many=True,
        )
        serialized_data = serializer.data
        return Response(serialized_data)


class UserStatisticsView(APIView):
    """
    Endpoint used by 10DS to get information about department signups
    """

    permission_classes = (
        IsAuthenticated,
        IsAPIUser,
    )

    def get(self, request):
        department_dict = get_learning_breakdown_data()
        serializer = DepartmentBreakdownSerializer(department_dict, many=True, partial=True, allow_null=True)
        serialized_data = serializer.data
        return Response(serialized_data)


def get_signups_by_date():
    """
    Calculates the number of signups per day
    @return: A dictionary containing a key for date, and value of number of signups
    """
    signups = (
        models.User.objects.annotate(signup_date=TruncDate("date_joined"))
        .values("signup_date")
        .annotate(
            count=Count("id", distinct=True),
            date_joined=Cast("signup_date", output_field=DateField()),
            number_of_signups=Cast("count", output_field=IntegerField()),
        )
        .values("date_joined", "number_of_signups")
    )

    return signups


def count_users_where(**kwargs):
    """expression builder to count users that fulfill some criteria"""
    expression = Count("learning__user__id", filter=Q(**kwargs), distinct=True)
    return expression


def get_learning_breakdown_data():
    """
    Calculates the number of signups per combination of department/grade/profession
    @return: A queryset that contains a list of each grouping
    """

    user_learning_times = models.User.objects.annotate(
        time_to_complete=Sum("learning__time_to_complete")
    ).order_by("department", "grade", "profession")


    class UserGroup:
        def __init__(self, user: models.User):
            self.department = user.department
            self.grade = user.grade
            self.profession = user.profession
            self.count = 1
            self.total_time_completed = user.time_to_complete or 0
            self.time_to_complete = [user.time_to_complete or 0]
            self.has_completed_pre_survey = user.has_completed_pre_survey
            self.has_completed_post_survey = user.has_completed_post_survey

        def add(self, user: models.User):
            self.count += 1
            self.total_time_completed += user.time_to_complete or 0
            self.time_to_complete.append(user.time_to_complete or 0)
            self.has_completed_pre_survey += int(user.has_completed_pre_survey)
            self.has_completed_post_survey += int(user.has_completed_post_survey)

        def completed(self, hours: int) -> int:
            return sum(1 for x in self.time_to_complete if x >= hours * 60)

        def to_dict(self):
            return {
            "department": self.department,
            "grade": self.grade,
            "profession": self.profession,
            "number_of_sign_ups": self.count,
            "total_time_completed": self.total_time_completed,
            "completed_first_evaluation": self.has_completed_pre_survey,
            "completed_second_evaluation": self.has_completed_post_survey,
            "completed_1_hours_of_learning": self.completed(1),
            "completed_2_hours_of_learning": self.completed(2),
            "completed_3_hours_of_learning": self.completed(3),
            "completed_4_hours_of_learning": self.completed(4),
            "completed_5_hours_of_learning": self.completed(5),
            "completed_6_hours_of_learning": self.completed(6),
            "completed_7_plus_hours_of_learning": self.completed(7),
        }

    d = {}
    for user in user_learning_times:
        group = user.department, user.grade, user.profession
        if group in d:
            d[group].add(user)
        else:
            d[group] = UserGroup(user)

    return [x.to_dict() for x in d.values()]




class JwtTokenObtainPairView(TokenObtainPairView):
    serializer_class = JwtTokenObtainPairSerializer
