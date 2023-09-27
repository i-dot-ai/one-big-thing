from django.db.models import Count, DateField, IntegerField, Q, Sum
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


def get_learning_breakdown_data():
    """
    Calculates the number of signups per combination of department/grade/profession
    @return: A queryset that contains a list of each grouping
    """

    # Count the total number of users in each group
    users_count_by_group = models.User.objects.values("department", "grade", "profession").annotate(
        number_of_sign_ups=Count("id"),
        total_time_completed=Coalesce(Cast(Sum("learning__time_to_complete"), IntegerField(default=0)) / 60, 0),
        completed_first_evaluation=Count("id", filter=Q(has_completed_pre_survey=True)),
        completed_second_evaluation=Count("id", filter=Q(has_completed_post_survey=True)),
        completed_1_hours_of_learning=Count("learning__user", filter=Q(learning__time_to_complete__gte=60)),
        completed_2_hours_of_learning=Count("learning__user", filter=Q(learning__time_to_complete__gte=120)),
        completed_3_hours_of_learning=Count("learning__user", filter=Q(learning__time_to_complete__gte=180)),
        completed_4_hours_of_learning=Count("learning__user", filter=Q(learning__time_to_complete__gte=240)),
        completed_5_hours_of_learning=Count("learning__user", filter=Q(learning__time_to_complete__gte=300)),
        completed_6_hours_of_learning=Count("learning__user", filter=Q(learning__time_to_complete__gte=360)),
        completed_7_plus_hours_of_learning=Count("learning__user", filter=Q(learning__time_to_complete__gte=420)),
    )

    return users_count_by_group


class JwtTokenObtainPairView(TokenObtainPairView):
    serializer_class = JwtTokenObtainPairSerializer
