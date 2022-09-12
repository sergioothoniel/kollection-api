from rest_framework import permissions


class InstitutionCustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):        
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated and request.user.role == 'Admin'

        return (
          request.user.is_authenticated
          and request.user.is_superuser
        )