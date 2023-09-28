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

    payload = []

    class UserGroup:
        def __init__(self, user):
            self.department = user.department
            self.grade = user.grade
            self.profession = user.profession
            self.time_to_complete = []
            self.has_completed_pre_survey = 0
            self.has_completed_post_survey = 0

        def add(self, user):
            self.time_to_complete += [user.time_to_complete or 0]
            self.has_completed_pre_survey += int(user.has_completed_pre_survey)
            self.has_completed_post_survey += int(user.has_completed_post_survey)

        def completed(self, minutes):
            return sum(1 for x in self.time_to_complete if x >= minutes)

    grouped_users = {}

    for user in user_learning_times:
        group = user.department, user.grade, user.profession
        if group not in grouped_users:
            grouped_users[group] = UserGroup(user)

        grouped_users[group].add(user)

    for (department, grade, profession), user_group in grouped_users.items():
        payload.append(
            {
                "department": department,
                "grade": grade,
                "profession": profession,
                "number_of_sign_ups": len(user_group.time_to_complete),
                "total_time_completed": sum(user_group.time_to_complete) / 60,
                "completed_first_evaluation": user_group.has_completed_pre_survey,
                "completed_second_evaluation": user_group.has_completed_post_survey,
                "completed_1_hours_of_learning": user_group.completed(1 * 60),
                "completed_2_hours_of_learning": user_group.completed(2 * 60),
                "completed_3_hours_of_learning": user_group.completed(3 * 60),
                "completed_4_hours_of_learning": user_group.completed(4 * 60),
                "completed_5_hours_of_learning": user_group.completed(5 * 60),
                "completed_6_hours_of_learning": user_group.completed(6 * 60),
                "completed_7_plus_hours_of_learning": user_group.completed(7 * 60),
            }
        )

    return payload


class JwtTokenObtainPairView(TokenObtainPairView):
    serializer_class = JwtTokenObtainPairSerializer
