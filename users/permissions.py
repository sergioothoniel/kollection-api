from rest_framework import permissions
from rest_framework.views import Request, View

from users.models import User


class DetailsUserPermissions(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, user: User):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.id == user.id


class AdminPermissions(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, user: User):

        return request.user.is_superuser or request.user.role == "Admin"
