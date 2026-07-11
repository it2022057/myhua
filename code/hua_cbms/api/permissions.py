from rest_framework import permissions

from accounts.checks import is_secretariat


class IsSecretariatUser(permissions.BasePermission):
    """
    Allows access only to secretariat users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            is_secretariat(request.user)
        )