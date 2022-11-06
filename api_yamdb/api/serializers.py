from rest_framework import serializers

from reviews.models import (Comment, Review,
                            Title, Category,
                            Genre, User)


class SingUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации."""

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        user = User.objects.create(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        return user


class ConfirmationCodeSerializer(serializers.Serializer):
    """Сериализатор для получения кода подтверждения"""

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена при регистрации."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        abstract = True
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class PersSerializer(UsersSerializer):
    """Сериализатор для пользователей"""
    role = serializers.CharField(read_only=True)


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

    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'rating', 'description',
            'genre', 'category')


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

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre',
                  'rating', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами"""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True, many=False,
    )
    score = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only = ('id',)


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания отзывов"""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,)
    score = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only = ('id',)

    def validate(self, data):
        request = self.context.get('request')
        title = self.context['view'].kwargs.get('title_id')

        if Review.objects.filter(
            author=request.user, title=title
        ).exists():
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
