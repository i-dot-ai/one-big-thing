from rest_framework import exceptions, serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from one_big_thing.learning.models import User


class JwtTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_api_user:
            raise exceptions.AuthenticationFailed("User does not have API access")

        return data


class DateJoinedSerializer(serializers.Serializer):
    date_joined = serializers.DateField()
    number_of_signups = serializers.IntegerField()

    class Meta:
        fields = [
            "date_joined",
            "number_of_signups",
        ]


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
    total_time_completed = serializers.IntegerField()

    class Meta:
        fields = [
            "department",
            "grade",
            "profession",
            "number_of_sign_ups",
            "completed_first_evaluation",
            "completed_second_evaluation",
            "completed_1_hours_of_learning",
            "completed_2_hours_of_learning",
            "completed_3_hours_of_learning",
            "completed_4_hours_of_learning",
            "completed_5_hours_of_learning",
            "completed_6_hours_of_learning",
            "completed_7_plus_hours_of_learning",
            "total_time_completed",
        ]
