from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Comment, Review, Title, Category, Genre


class UsersSerializer(serializers.ModelSerializer):
    pass


class NotAdminSerializer(serializers.ModelSerializer):
    pass


class GetTokenSerializer(serializers.ModelSerializer):
    pass


class SignUpSerializer(serializers.ModelSerializer):
    pass


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий (типов) произведений."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для возврата списка произведений."""

    category = CategorySerializer()
    genre = GenreSerializer(
        many=True,
        read_only=True
    )
    year = serializers.IntegerField()

    class Meta:
        fields = ('category', 'genre', 'name', 'year')
        model = Title


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
    year = serializers.IntegerField()

    class Meta:
        fields = ('name', 'year', 'description',
                  'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами"""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only = ('id',)

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError(
                'Оценка по 10-бальной шкале!'
            )
        return value

    def validate(self, data):
        request = self.context.get('request')
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(
                author=request.user, title=title
            ).exists()
        ):
            raise serializers.ValidationError(
                'Вы уже оставили отзыв!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с комментариями."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
