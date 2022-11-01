from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import get_object_or_404

from .permissions import IsAuthorOrModeratorOrAdminOrReadOnly
from .serializers import (CommentSerializer,
                          ReviewSerializer)
from .mixins import CreateListViewSet
from reviews.models import Review, Title


class UsersViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(CreateListViewSet):
    pass


class GenreViewSet(CreateListViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Получить список всех отзывов.
    Права доступа: Доступно авторизованным юзерам.
    """
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdminOrReadOnly
    )
    pagination_class = PageNumberPagination

    def get_title(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
    
    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """
    Получить список всех комментариев. 
    Права доступа: Доступно авторизованным юзерам.
    """
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdminOrReadOnly
    )
    pagination_class = PageNumberPagination

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self.get_review()
        )
