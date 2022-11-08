from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import (permissions, viewsets,
                            views, filters,
                            response, status)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404

from .filters import FilterForTitle
from .permissions import (IsAdmin, IsAuthorOrModeratorOrAdminOrReadOnly,
                          IsAdminOrReadOnly)
from .serializers import (ConfirmationCodeSerializer,
                          CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          PersSerializer, ReviewCreateSerializer,
                          SingUpSerializer, TitleReadSerializer,
                          TitleWriteSerializer, UsersSerializer)
from .mixins import CreateListDestroyViewSet
from reviews.models import Category, Genre, Review, Title, User


def sent_confirmation_code(request):
    """Функция отправки кода подтверждения при регистрации."""
    user = get_object_or_404(User, email=request.data["email"])
    confirmation_code = get_random_string()
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        subject="Код для генерации токена аутентификации",
        message=str(confirmation_code),
        from_email=settings.LENG_EMAIL,
        recipient_list=(request.data["email"],),
    )
    return response.Response(
        data="Письмо с кодом для аутентификации",
        status=status.HTTP_201_CREATED,
    )


class SignUp(views.APIView):
    """Функция регистрации новых пользователей."""

    serializer_class = SingUpSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        sent_confirmation_code(request)
        return response.Response(request.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    """Функция получения токена при регистрации."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.validated_data.get('confirmation_code')
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return response.Response(
            {'token': str(token)}, status=status.HTTP_200_OK
        )
    return response.Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    search_fields = ('username', )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = PersSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response(
                serializer.data, status=status.HTTP_200_OK
            )
        serializer = PersSerializer(user)
        return response.Response(
            serializer.data, status=status.HTTP_200_OK
        )


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Отображение действий с жанрами для произведений."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для произведений.
    Для запросов на чтение используется TitleReadSerializer
    Для запросов на изменение используется TitleWriteSerializer
    """
    queryset = Title.objects.order_by('name').all().annotate(
        Avg('reviews__score')
    )
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    filterset_class = FilterForTitle

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Отображение действий с отзывами."""

    serializer_class = ReviewCreateSerializer
    permission_classes = (
        IsAuthorOrModeratorOrAdminOrReadOnly,
    )

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
    """Отображение действий с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrModeratorOrAdminOrReadOnly,
    )

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self.get_review()
        )
