from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from .permissions import IsAdminOrReadOnly


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    pagination_class = PageNumberPagination
    search_fields = ['name']
    lookup_field = 'slug'
