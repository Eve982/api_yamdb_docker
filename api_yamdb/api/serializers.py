from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Avg, IntegerField
from rest_framework import serializers
from datetime import datetime

from reviews.models import (Comment, Review,
                            Title, Category,
                            Genre, User)
from reviews.models import username_me


class SingUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""

    email = serializers.EmailField(required=True)
    username = serializers.RegexField(
        max_length=settings.LENG_DATA_USER,
        regex=r'^[\w.@+-]+\Z', required=True
    )

    def validate_username(self, value):
        return username_me(value)

class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена при регистрации."""

    username = serializers.RegexField(max_length=settings.LENG_DATA_USER,
                                      regex=r'^[\w.@+-]+\Z', required=True,)
    confirmation_code = serializers.CharField(required=True)

    def validate_username(self, value):
        return username_me(value)


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        abstract = True
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class PersSerializer(UsersSerializer):
    """Сериализатор для пользователей."""

    class Meta(UsersSerializer.Meta):
        read_only_fields = ('role', )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий (типов) произведений."""

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для возврата списка произведений."""

    rating = serializers.SerializerMethodField(
        read_only=True,
    )
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'rating', 'description',
            'genre', 'category')
        read_only_fields = (
            'id', 'name', 'year',
            'rating', 'description',
            'genre', 'category')

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg(
            'score',
            output_field=IntegerField())
        )['score__avg']


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления произведений."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    rating = serializers.IntegerField(required=False)
    year = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre',
                  'rating', 'category')

    def to_representation(self, instance):
        return TitleReadSerializer(instance).data

    def validate_year(self, data):
        if data >= datetime.now().year:
            raise serializers.ValidationError(
                f'Год {data} больше текущего!',
            )
        return data


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True, many=False,)
    score = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only = ('id',)

    def validate(self, data):
        request = self.context.get('request')
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)

        if (
            request.method == 'POST' and Review.objects.filter(
                author=request.user, title=title
            ).exists()
        ):
            raise serializers.ValidationError(
                'Вы уже оставили отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с комментариями."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only = ('id',)
