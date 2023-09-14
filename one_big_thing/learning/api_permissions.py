from rest_framework.permissions import BasePermission


class IsAPIUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_api_user
