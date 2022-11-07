from rest_framework import permissions


class IsAdmin(permissions.IsAdminUser):
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
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )


# class UsersPermission(permissions.BasePermission):
#     """Разрешения для действий с пользователями для пользователей."""

#     def has_permission(self, request, view):
#         return request.user.is_authenticated

#     def has_object_permission(self, view, request, obj):
#         return request.method in ('PATCH', 'GET')
