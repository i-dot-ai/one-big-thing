from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from one_big_thing.api_serializers import (
    MyTokenObtainPairSerializer,
    UserSerializer,
)
from one_big_thing.learning.api_permissions import IsAPIUser
from one_big_thing.learning.models import User


class UserViewSet(
    GenericViewSet, RetrieveModelMixin, ListModelMixin
):  # allows GETs for many, GET for one and generic view functionality
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAPIUser,)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
