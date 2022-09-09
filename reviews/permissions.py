import ipdb
from rest_framework import permissions
from rest_framework.views import Request, View


class ReviewViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.role == "Professor"


class ReviewUpdateDestroyPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.id == obj.user.id
