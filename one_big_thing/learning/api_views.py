import json

from django.db import connection
from django.db.models import Case, Count, DateField, IntegerField, Sum, When, Value
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
    groupings = models.User.objects.values("department", "grade", "profession").annotate(
        total_time_completed=Coalesce(Cast(Sum("learning__time_to_complete"), IntegerField(default=0)) / 60, 0),
        number_of_sign_ups=Count("id", distinct=True),
        completed_first_evaluation=Count(
            Case(
                When(
                    has_completed_pre_survey=True,
                    then=Value(1),
                ),
            ),
        ),
        completed_second_evaluation=Count(
            Case(
                When(
                    has_completed_post_survey=True,
                    then=Value(1),
                ),
            ),
        ),
        **{
            f"completed_{i}_hours_of_learning": Case(
                When(total_time_completed__gte=i, then=1), default=0, output_field=IntegerField()
            )
            for i in range(1, 7)
        },
        completed_7_plus_hours_of_learning=Case(
            When(total_time_completed__gte=7, then=1), default=0, output_field=IntegerField()
        ),
    )
    return groupings.distinct()


class TestView(APIView):
    """
    Endpoint used by 10DS to get information about department signups
    """

    permission_classes = (
        IsAuthenticated,
        IsAPIUser,
    )

    def get(self, request):
        data = run_raw_sql()
        return Response(data)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def run_raw_sql():
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT
                DATE(date_joined) as date_joined,
                department,
                grade,
                profession,
                count(*) as number_of_sign_ups,
                count(CASE WHEN u.has_completed_pre_survey THEN 1 END) as completed_first_evaluation,
                count(CASE WHEN u.has_completed_post_survey THEN 1 END) as completed_second_evaluation,
                sum(l.completed_1_hours_of_learning) as completed_1_hours_of_learning,
                sum(l.completed_2_hours_of_learning) as completed_2_hours_of_learning,
                sum(l.completed_3_hours_of_learning) as completed_3_hours_of_learning,
                sum(l.completed_4_hours_of_learning) as completed_4_hours_of_learning,
                sum(l.completed_5_hours_of_learning) as completed_5_hours_of_learning,
                sum(l.completed_6_hours_of_learning) as completed_6_hours_of_learning,
                sum(l.completed_7_plus_hours_of_learning) as completed_7_plus_hours_of_learning
            FROM public.learning_user as u
            LEFT JOIN (
                SELECT
                    user_id,
                    CASE
                        WHEN hours_learning > 1  THEN 1
                        ELSE 0
                        END as completed_1_hours_of_learning,
                    CASE
                        WHEN hours_learning > 2  THEN 1
                        ELSE 0
                    END as completed_2_hours_of_learning,
                    CASE
                        WHEN hours_learning > 3  THEN 1
                        ELSE 0
                    END as completed_3_hours_of_learning,
                    CASE
                        WHEN hours_learning > 4  THEN 1
                        ELSE 0
                    END as completed_4_hours_of_learning,
                    CASE
                        WHEN hours_learning > 5  THEN 1
                        ELSE 0
                    END as completed_5_hours_of_learning,
                    CASE
                        WHEN hours_learning > 6  THEN 1
                        ELSE 0
                    END as completed_6_hours_of_learning,
                    CASE
                        WHEN hours_learning > 7  THEN 1
                        ELSE 0
                    END as completed_7_plus_hours_of_learning
                    FROM (
                        SELECT
                            sum(time_to_complete)/60 as hours_learning,
                            user_id
                        FROM public.learning_learning
                        GROUP BY user_id
                    ) inner_l
            ) l
            ON l.user_id = u.id
            GROUP BY department,
                grade,
                profession,
                date_joined"""
        )
        rows = dictfetchall(cursor)
        return rows
    # cursor = connection.cursor()
    # cursor.execute(
    #     """"""
    # )
    # rows = cursor.fetchall()
    # print(type(rows[0][0]))
    # all_rows = json.dumps(rows, indent=4, sort_keys=True, default=str)
    # return all_rows


class JwtTokenObtainPairView(TokenObtainPairView):
    serializer_class = JwtTokenObtainPairSerializer
