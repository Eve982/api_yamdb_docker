from rest_framework import permissions


class IsAdmin(permissions.IsAdminUser):
    """Права для работы с пользователями."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_staff
            or request.user.is_superuser
        )


class IsAuthorOrModeratorOrAdminOrReadOnly(
    permissions.IsAuthenticatedOrReadOnly
):
    """Права для работы с отзывами и комментариями."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права для работы с категориями и жанрами."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )
