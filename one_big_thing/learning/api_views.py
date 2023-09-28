import itertools

from django.db.models import Count, DateField, IntegerField, Sum
from django.db.models.functions import Cast, TruncDate
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


def get_learning_breakdown_data():
    """
    Calculates the number of signups per combination of department/grade/profession
    @return: A queryset that contains a list of each grouping
    """

    user_learning_times = models.User.objects.annotate(time_to_complete=Sum("learning__time_to_complete")).order_by(
        "department", "grade", "profession"
    )

    def completed(times_to_complete: list[int], hours: int) -> int:
        return sum(1 for time in times_to_complete if time >= hours * 60)

    for (department, grade, profession), users in itertools.groupby(
        user_learning_times, key=lambda x: (x.department, x.grade, x.profession)
    ):
        time_to_complete = []
        count = 0
        has_completed_pre_survey = 0
        has_completed_post_survey = 0
        for user in users:
            count += 1
            time_to_complete.append(user.time_to_complete or 0)
            has_completed_pre_survey += user.has_completed_pre_survey
            has_completed_post_survey += user.has_completed_post_survey

        yield {
            "department": department,
            "grade": grade,
            "profession": profession,
            "number_of_sign_ups": count,
            "total_time_completed": sum(time_to_complete) / 60,
            "completed_first_evaluation": has_completed_pre_survey,
            "completed_second_evaluation": has_completed_post_survey,
            "completed_1_hours_of_learning": completed(time_to_complete, 1),
            "completed_2_hours_of_learning": completed(time_to_complete, 2),
            "completed_3_hours_of_learning": completed(time_to_complete, 3),
            "completed_4_hours_of_learning": completed(time_to_complete, 4),
            "completed_5_hours_of_learning": completed(time_to_complete, 5),
            "completed_6_hours_of_learning": completed(time_to_complete, 6),
            "completed_7_plus_hours_of_learning": completed(time_to_complete, 7),
        }


class JwtTokenObtainPairView(TokenObtainPairView):
    serializer_class = JwtTokenObtainPairSerializer
