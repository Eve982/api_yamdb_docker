from rest_framework import permissions


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return request.method in permissions.SAFE_METHODS or (
            (user == obj.author)
            or user.is_admin or user.is_moderator
        )
