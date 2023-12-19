from functools import reduce

from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from one_big_thing.learning.models import (
    POST_SURVEY_TYPES,
    PRE_SURVEY_TYPES,
    User,
)
from one_big_thing.learning.survey_handling import questions_data


class JwtTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_api_user:
            raise exceptions.AuthenticationFailed("User does not have API access")

        return data


class DateJoinedSerializer(serializers.Serializer):
    date_joined = serializers.DateField()
    number_of_signups = serializers.IntegerField()
    department = serializers.CharField(source="department__code")
    parent = serializers.CharField(source="department__parent")

    class Meta:
        fields = ["__all__"]


class DepartmentBreakdownSerializer(serializers.Serializer):
    department = serializers.CharField(allow_null=True)
    grade = serializers.CharField(allow_null=True)
    profession = serializers.CharField(allow_null=True)
    number_of_sign_ups = serializers.IntegerField()
    completed_first_evaluation = serializers.IntegerField()
    completed_second_evaluation = serializers.IntegerField()
    completed_1_hours_of_learning = serializers.IntegerField()
    completed_2_hours_of_learning = serializers.IntegerField()
    completed_3_hours_of_learning = serializers.IntegerField()
    completed_4_hours_of_learning = serializers.IntegerField()
    completed_5_hours_of_learning = serializers.IntegerField()
    completed_6_hours_of_learning = serializers.IntegerField()
    completed_7_plus_hours_of_learning = serializers.IntegerField()

    class Meta:
        fields = "__all__"


class NormalizedDepartmentBreakdownSerializer(serializers.Serializer):
    department = serializers.CharField(allow_null=True, source="department__code")
    grade = serializers.CharField(allow_null=True)
    profession = serializers.CharField(allow_null=True)
    user_count = serializers.IntegerField()
    has_completed_pre_survey = serializers.BooleanField()
    has_completed_post_survey = serializers.BooleanField()
    bucketed_hours = serializers.CharField()

    class Meta:
        fields = "__all__"


class DepartmentCompletionStatisticsSerializer(serializers.Serializer):
    department = serializers.CharField(allow_null=True, source="user__department__code")
    parent_department = serializers.CharField(allow_null=True, source="user__department__parent")
    total_hours = serializers.IntegerField()
    recorded_on = serializers.DateField()

    class Meta:
        fields = "__all__"


class LearningSerializer(serializers.Serializer):
    title = serializers.CharField()
    learning_type = serializers.CharField()
    rating = serializers.IntegerField()
    link = serializers.URLField()
    time_to_complete = serializers.IntegerField()


def build_empty_survey_dict(*keys: str) -> dict[str, str]:
    empty_dict = {}
    for key, questions_set in questions_data.items():
        if key in keys:
            for questions in questions_set:
                for question in questions["questions"]:
                    empty_dict[question["id"]] = ""
    return empty_dict


class SurveyParticipantSerializer(serializers.Serializer):
    department = serializers.CharField()
    grade = serializers.CharField()
    profession = serializers.CharField()
    learning_records = LearningSerializer(many=True, source="learning_set")

    def to_representation(self, instance: User):
        representation = super().to_representation(instance)

        empty_pre_survey_dict = build_empty_survey_dict(*PRE_SURVEY_TYPES)
        representation["pre"] = reduce(
            lambda x, y: x | y,
            instance.pre_survey_results.values_list("data", flat=True),
            empty_pre_survey_dict,
        )

        empty_post_survey_dict = build_empty_survey_dict(*POST_SURVEY_TYPES)
        representation["post"] = reduce(
            lambda x, y: x | y,
            instance.post_survey_results.values_list("data", flat=True),
            empty_post_survey_dict,
        )

        return representation
