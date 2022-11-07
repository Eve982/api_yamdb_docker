from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    validate_slug)
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from .validators import validate_year, validate_username


class GenreAndCategoryModel(models.Model):
    """Абстрактная модель. Добавляет слаг и название."""

    slug = models.SlugField(
        'Slug',
        max_length=settings.LENG_SLUG,
        unique=True,
        validators=[validate_slug],
    )
    name = models.CharField(
        'Название',
        max_length=settings.LENG_MAX,
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name[:settings.LENG_CUT]


class ReviewAndCommentModel(models.Model):
    """Абстрактная модель. Добавляет текст, автора и дату публикации."""

    text = models.CharField(
        'Текст отзыва',
        max_length=settings.LENG_MAX
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:settings.LENG_CUT]


class User(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLE_CHOICES = [
        (USER, USER),
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
    ]

    username = models.CharField(
        'Имя пользователя',
        validators=(validate_username,),
        max_length=settings.LENG_DATA_USER,
        unique=True,
        blank=False,
        null=False,
        help_text='Набор символов не более 30.'
                  'Только буквы, цифры и @/./+/-/_',
        error_messages={
            'unique': "Пользователь с таким именем уже существует!",
        },
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=settings.LENG_EMAIL,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'Роль',
        max_length=settings.LENG_CUT,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    REQUIRED_FIELDS = ['email', ]

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email',
            )
        ]

    def __str__(self):
        return f'{self.username} {self.email} {self.role}'


class Category(GenreAndCategoryModel):
    """Модель категории(типа) произведения."""

    class Meta(GenreAndCategoryModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'categories'


class Genre(GenreAndCategoryModel):
    """Модель жанра произведений."""

    class Meta(GenreAndCategoryModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = 'genres'


class Title(models.Model):
    """Модель произведения."""

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.PROTECT,
        related_name='titles',
    )
    description = models.TextField(
        'Описание',
        db_index=True,
        max_length=settings.LENG_MAX,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
    )
    name = models.CharField(
        'Название',
        max_length=settings.LENG_MAX,
        db_index=True,
    )
    year = models.IntegerField(
        'Год выпуска',
        db_index=True,
        validators=(validate_year,),
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(ReviewAndCommentModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.IntegerField(
        'Оценка',
        db_index=True,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={
            'validators': 'Оценка от 1 до 10!'
        },
        default=1
    )

    class Meta(ReviewAndCommentModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review',
            )
        ]


class Comment(ReviewAndCommentModel):
    """Модель комментария к отзыву."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(ReviewAndCommentModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
