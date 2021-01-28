from rest_framework.permissions import BasePermission


class HasAccountPermission(BasePermission):

    def has_permission(self, request, view):
        return request.account is not None
