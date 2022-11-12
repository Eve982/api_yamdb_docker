from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from .permissions import IsAdminOrReadOnly


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Миксин для Category/Genre ViewSet."""
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    pagination_class = PageNumberPagination
    search_fields = ['name']
    lookup_field = 'slug'
