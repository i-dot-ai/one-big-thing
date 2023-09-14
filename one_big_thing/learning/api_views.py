from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from one_big_thing.api_serializers import (
    JwtTokenObtainPairSerializer,
    EntitySerializer,
)
from one_big_thing.learning.api_permissions import IsAPIUser


class UserStatisticsView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsAPIUser,
    )

    def get(self, request):
        # Create a dictionary
        # For each user
        # Add or insert to department entry
        # Add or insert to date joined (do we want this before or after department)
        # Add or insert to Profession entry
        # Add or insert to Grade entry
        # Add no of logins etc (how to combine)

        entities = [
            {"field1": "value1", "field2": 123},
            {"field1": "value2", "field2": 456},
        ]
        serializer = EntitySerializer(entities, many=True)
        serialized_data = serializer.data
        return Response(serialized_data)


class JwtTokenObtainPairView(TokenObtainPairView):
    serializer_class = JwtTokenObtainPairSerializer
