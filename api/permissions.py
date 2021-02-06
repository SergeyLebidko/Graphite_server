from rest_framework.permissions import BasePermission, SAFE_METHODS


class HasAccountPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        return request.account is not None


class HasPostPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.account is not None
