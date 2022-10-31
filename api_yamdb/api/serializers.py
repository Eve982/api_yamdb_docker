from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User


class UsersSerializer(serializers.ModelSerializer):
    pass


class NotAdminSerializer(serializers.ModelSerializer):
    pass


class GetTokenSerializer(serializers.ModelSerializer):
    pass


class SignUpSerializer(serializers.ModelSerializer):
    pass


class CategorySerializer(serializers.ModelSerializer):
    pass


class GenreSerializer(serializers.ModelSerializer):
    pass


class TitleReadSerializer(serializers.ModelSerializer):
    pass


class TitleWriteSerializer(serializers.ModelSerializer):
    pass


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
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value

    def validate(self, data):
        request = self.context.get('request')
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(author=request.user, title=title).exists()
        ):
            raise serializers.ValidationError('Вы уже оставили отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    pass
