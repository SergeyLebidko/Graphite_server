from rest_framework.permissions import BasePermission


class HasAccountPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        return request.account is not None
