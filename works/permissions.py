from rest_framework import permissions

from works.models import Work


class WorkViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated


class IsWorkOwnerOrInternOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, work: Work):

        if request.method in permissions.SAFE_METHODS:
            if work.visibility == "Public":
                return True
            return request.user.institution_id == work.users.all()[0].institution.id

        ids = [work_dict.id for work_dict in work.users.all()]

        if request.user.id in ids:
            return True
        return False
