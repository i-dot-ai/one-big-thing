from django.db.models import Case, Count, IntegerField, Sum, When
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
    signups = {}

    user_counts = (
        models.User.objects.annotate(signup_date=TruncDate("date_joined"))
        .values("signup_date")
        .annotate(count=Count("id"))
    )

    for user_count in user_counts:
        signup_date = user_count["signup_date"].strftime("%d/%m/%Y")
        count = user_count["count"]
        signups[signup_date] = count
    signups = [{"date_joined": k, "number_of_signups": v} for k, v in signups.items()]
    return signups


def get_learning_breakdown_data():
    groupings = models.User.objects.values("department", "grade", "profession").annotate(
        total_time_completed=Coalesce(Cast(Sum("learning__time_to_complete"), IntegerField(default=0)) / 60, 0),
        number_of_sign_ups=Cast(Sum(1), IntegerField()),
        completed_first_evaluation=Case(
            When(has_completed_pre_survey=True, then=1), default=0, output_field=IntegerField()
        ),
        completed_second_evaluation=Case(
            When(has_completed_post_survey=True, then=1), default=0, output_field=IntegerField()
        ),
        **{
            f"completed_{i}_hours_of_learning": Case(
                When(total_time_completed=i, then=1), default=0, output_field=IntegerField()
            )
            for i in range(1, 7)
        },
        completed_7_plus_hours_of_learning=Case(
            When(total_time_completed__gte=7, then=1), default=0, output_field=IntegerField()
        ),
    )
    return groupings


class JwtTokenObtainPairView(TokenObtainPairView):
    serializer_class = JwtTokenObtainPairSerializer
