from rest_framework import viewsets

from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          NotAdminSerializer, ReviewSerializer,
                          SignUpSerializer, TitleReadSerializer,
                          TitleWriteSerializer, UsersSerializer)
from .mixins import CreateListViewSet
from reviews.models import Category, Genre, Review, Title


class UsersViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(CreateListViewSet):
    pass


class GenreViewSet(CreateListViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass
