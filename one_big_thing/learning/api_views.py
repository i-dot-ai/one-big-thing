from django.db.models import (
    Case,
    Count,
    DateField,
    IntegerField,
    Sum,
    Value,
    When,
)
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
        total_time_completed=Coalesce(
            Cast(Sum("learning__time_to_complete", distinct=True), IntegerField(default=0)) / 60, 0
        ),
        number_of_sign_ups=Count("id", distinct=True),
        completed_first_evaluation=Count(
            Case(When(has_completed_pre_survey=True, then=1), default=0),
            distinct=True,
            output_field=IntegerField(default=0),
        ),
        completed_second_evaluation=Count(
            Case(
                When(
                    has_completed_post_survey=True,
                    then=Value(1),
                ),
            ),
            distinct=True,
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

    # groupings = (
    #     models.User.objects.annotate(
    #         completed_first_evaluation=Case(
    #             When(has_completed_pre_survey=True, then=Value(1)), default=Value(0), output_field=IntegerField()
    #         ),
    #         completed_second_evaluation=Case(
    #             When(has_completed_post_survey=True, then=Value(1)), default=Value(0), output_field=IntegerField()
    #         ),
    #     )
    #     .values("department", "grade", "profession", "completed_first_evaluation", "completed_second_evaluation")
    #     .annotate(
    #         total_time_completed=Coalesce(
    #             Cast(Sum("learning__time_to_complete", distinct=True), IntegerField(default=0)) / 60, 0
    #         ),
    #         number_of_sign_ups=Count("id", distinct=True),
    #         completed_first_evaluation_count=Sum("completed_first_evaluation"),
    #         completed_second_evaluation_count=Sum("completed_second_evaluation"),
    #         **{
    #             f"completed_{i}_hours_of_learning": Case(
    #                 When(total_time_completed__gte=i, then=1), default=0, output_field=IntegerField()
    #             )
    #             for i in range(1, 7)
    #         },
    #         completed_7_plus_hours_of_learning=Case(
    #             When(total_time_completed__gte=7, then=1), default=0, output_field=IntegerField()
    #         ),
    #     )
    # )

    # groupings = models.User.objects.values("department", "grade", "profession")
    #
    # groupings = models.User.objects.annotate(
    #     completed_first_evaluation_count=Case(
    #         When(has_completed_pre_survey=True, then=Value(1)), default=Value(0), output_field=IntegerField()
    #     ),
    #     completed_second_evaluation_count=Case(
    #         When(has_completed_post_survey=True, then=Value(1)), default=Value(0), output_field=IntegerField()
    #     ),
    # )
    #
    # # Then, group by department, grade, and profession
    # groupings = groupings.values("department", "grade", "profession").annotate(
    #     number_of_sign_ups=Count("id"),
    #     total_time_completed=Coalesce(
    #         Cast(Sum("learning__time_to_complete", distinct=True), IntegerField(default=0)) / 60, 0
    #     ),
    #     completed_first_evaluation=Sum("completed_first_evaluation_count"),
    #     completed_second_evaluation=Sum("completed_second_evaluation_count"),
    #     **{
    #         f"completed_{i}_hours_of_learning": Case(
    #             When(total_time_completed__gte=i, then=1), default=0, output_field=IntegerField()
    #         )
    #         for i in range(1, 7)
    #     },
    #     completed_7_plus_hours_of_learning=Case(
    #         When(total_time_completed__gte=7, then=1), default=0, output_field=IntegerField()
    #     ),
    # )
    return groupings


class JwtTokenObtainPairView(TokenObtainPairView):
    serializer_class = JwtTokenObtainPairSerializer
