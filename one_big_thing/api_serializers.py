from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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


SURVEY_FIELDS = {
    "pre": [
        "confident-in-decisions",
        "confidence-graphic-survey",
        "confidence-explaining-chart",
        "confident-day-to-day",
        "data-support-day-to-day",
        "data-is-relevant-to-role",
        "use-data-effectively-day-to-day",
        "line-manager",
        "help-team",
        "coach-team",
        "support-team",
        "training-last-six-months",
        "training-analytical-component",
        "aware-of-the-aims",
        "shared-identity",
        "identity-is-important",
    ],
    "post": [
        "training-level",
        "shared-identity",
        "identity-important",
        "confident-day-to-day",
        "data-support-day-to-day",
        "data-is-relevant-to-role",
        "use-data-effectively-day-to-day",
        "line-manager",
        "help-team",
        "coach-team",
        "support-team",
        "anticipate-data-limitations",
        "understanding-ethics-for-data",
        "understand-how-to-quality-assure-data",
        "more-effectively-communicate-data-insights-to-improve-decisions",
        "find-mentor",
        "book-training",
        "other-development",
        "create-development-plan",
        "add-learning-to-development-plan",
        "training-helped-learning",
        "conversations-helped-learning",
        "additional-resources-helped-learning",
        "useful-learning-formats",
        "obt-good-use-of-time",
        "content-was-relevant-to-my-role",
        "intend-to-apply-learning-in-my-role",
        "improved-understanding-of-using-data",
        "intend-to-participate-in-further-training",
        "aware-of-aims",
        "sufficient-time",
        "what-went-well",
        "what-can-be-improved",
        "willing-to-follow-up",
    ],
}


class SurveyParticipantSerializer(serializers.Serializer):
    department = serializers.CharField()
    grade = serializers.CharField()
    profession = serializers.CharField()
    learning_records = LearningSerializer(many=True, source="learning_set")

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        for survey_type, survey_keys in SURVEY_FIELDS.items():
            condensed_survey = dict.fromkeys(survey_keys, "")
            for survey in instance.surveyresult_set.filter(survey_type=survey_type).all().values():
                condensed_survey = condensed_survey | survey['data']
            representation[survey_type] = condensed_survey

        return representation
