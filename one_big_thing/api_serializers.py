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
