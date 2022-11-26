from rest_framework import permissions

from core.constants import ADMIN, MODERATOR


def is_admin(self, user):
    return user.role == ADMIN


def is_moderator(self, user):
    return user.role == MODERATOR


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return self.is_admin(request.user) or request.user.is_superuser


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return self.is_moderator(request.user)
