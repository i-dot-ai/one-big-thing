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


class EntitySerializer(serializers.Serializer):
    field1 = serializers.CharField()
    field2 = serializers.IntegerField()

    class Meta:
        fields = ["field1", "field2"]
