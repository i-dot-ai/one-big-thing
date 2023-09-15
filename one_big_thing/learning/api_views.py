from collections import defaultdict

from django.db.models import Case, Count, IntegerField, Sum, When
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
    department_dict = defaultdict()

    users = models.User.objects.annotate(
        total_time_completed=Cast(Sum("learning__time_to_complete"), IntegerField()),
        total_time_completed_trimmed=Cast(Sum("learning__time_to_complete"), IntegerField()) / 60,
        completed_first_evaluation=Case(
            When(has_completed_pre_survey=True, then=1), default=0, output_field=IntegerField()
        ),
        completed_second_evaluation=Case(
            When(has_completed_post_survey=True, then=1), default=0, output_field=IntegerField()
        ),
        **{
            f"completed_{i}_hours_of_learning": Case(
                When(total_time_completed_trimmed=i, then=1), default=0, output_field=IntegerField()
            )
            for i in range(1, 7)
        },
        completed_7_plus_hours_of_learning=Case(
            When(total_time_completed_trimmed=7, then=1), default=0, output_field=IntegerField()
        ),
    )

    for user in users:
        department = user.department
        grade = user.grade
        profession = user.profession

        if (department, grade, profession) not in department_dict:
            department_dict[(department, grade, profession)] = {
                "total_time_completed": 0,
                "number_of_sign_ups": 0,
                "completed_first_evaluation": 0,
                "completed_second_evaluation": 0,
                **{f"completed_{i}_hours_of_learning": 0 for i in range(1, 7)},
                "completed_7_plus_hours_of_learning": 0,
            }

        department_dict[(department, grade, profession)]["total_time_completed"] += (
            user.total_time_completed if user.total_time_completed else 0
        )
        department_dict[(department, grade, profession)]["number_of_sign_ups"] += 1
        department_dict[(department, grade, profession)][
            "completed_first_evaluation"
        ] += user.completed_first_evaluation
        department_dict[(department, grade, profession)][
            "completed_second_evaluation"
        ] += user.completed_second_evaluation
        for i in range(1, 7):
            department_dict[(department, grade, profession)][f"completed_{i}_hours_of_learning"] += getattr(
                user, f"completed_{i}_hours_of_learning"
            )
        department_dict[(department, grade, profession)][
            "completed_7_plus_hours_of_learning"
        ] += user.completed_7_plus_hours_of_learning

    department_dict = [
        {
            "department": k[0],
            "grade": k[1],
            "profession": k[2],
            **v,
            "total_time_completed": (v["total_time_completed"] / 60),
        }
        for k, v in department_dict.items()
    ]
    return department_dict


class JwtTokenObtainPairView(TokenObtainPairView):
    serializer_class = JwtTokenObtainPairSerializer
