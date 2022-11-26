from rest_framework import permissions

from core.constants import ADMIN, MODERATOR


def is_admin(obj):
    return obj.role == ADMIN


def is_moderator(obj):
    return obj.role == MODERATOR


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return is_admin(request.user) or request.user.is_superuser


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return is_moderator(request.user)
