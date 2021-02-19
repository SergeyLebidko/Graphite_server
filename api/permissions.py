from rest_framework.permissions import BasePermission, SAFE_METHODS


class CustomBasePermission(BasePermission):
    allowed_methods = None

    def has_permission(self, request, view):
        if not self.allowed_methods:
            return False
        if request.method in self.allowed_methods:
            return True
        return request.account is not None


class HasAccountPermission(CustomBasePermission):
    allowed_methods = ['OPTIONS']


class HasPostPermission(CustomBasePermission):
    allowed_methods = SAFE_METHODS


class HasCommentPermission(CustomBasePermission):
    allowed_methods = SAFE_METHODS
