from collections import defaultdict
from datetime import datetime

from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from one_big_thing.api_serializers import (
    DepartmentBreakdownSerializer,
    JwtTokenObtainPairSerializer,
    DateJoinedSerializer,
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
        signups = [{"date_joined": k, "number_of_signups": v} for k, v in signups.items()]
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
        department_dict = defaultdict(lambda: defaultdict(int))
        department_dict = get_learning_breakdown_data(department_dict)
        final_dict = [{"department": k[0], "grade": k[1], "profession": k[2], **v} for k, v in department_dict.items()]
        serializer = DepartmentBreakdownSerializer(final_dict, many=True, partial=True, allow_null=True)
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
    return signups


def get_learning_breakdown_data(department_dict):
    for user in models.User.objects.all():
        department = user.department
        grade = user.grade
        profession = user.profession

        learning_records = user.learning_set.all()
        total_hours_completed = sum([record.time_to_complete for record in learning_records])
        department_dict[(department, grade, profession)]["total_time_completed"] += total_hours_completed
        department_dict[(department, grade, profession)]["number_of_sign_ups"] += 1
        department_dict[(department, grade, profession)]["completed_first_evaluation"] += (
            1 if user.has_completed_pre_survey else 0
        )
        department_dict[(department, grade, profession)]["completed_second_evaluation"] += (
            1 if user.has_completed_post_survey else 0
        )
        for i in range(1, 7):
            department_dict[(department, grade, profession)][f"completed_{i}_hours_of_learning"] += (
                1 if total_hours_completed / 60 == i else 0
            )
        department_dict[(department, grade, profession)][f"completed_7_plus_hours_of_learning"] += (
            1 if total_hours_completed / 60 >= 7 else 0
        )

    for k, v in department_dict.items():
        department_dict[k]["total_time_completed"] = department_dict[k]["total_time_completed"] / 60

    return department_dict


class JwtTokenObtainPairView(TokenObtainPairView):
    serializer_class = JwtTokenObtainPairSerializer
