from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import validate_year

# class User(AbstractUser):
#     pass


class Category(models.Model):
    """Модель категории(типа) произведения."""

    slug = models.SlugField(
        'Slug категории',
        max_length=50,
        unique=True,
    )
    name = models.CharField(
        'Название категории',
        max_length=256,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведений."""

    slug = models.SlugField(
        'Slug жанра',
        max_length=50,
        unique=True,
    )
    name = models.CharField(
        'Название жанра',
        max_length=256,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True,
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
    )
    rating = models.IntegerField(
        'Рейтинг произведения',
        default=None,
        null=True,
        blank=True,
    )
    name = models.CharField(
        'Название',
        max_length=200,
        db_index=True,
    )
    year = models.DateTimeField(
        'Год выпуска',
        blank=True,
        validators=(validate_year,)
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов на произведение."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.CharField(
        'Текст отзыва',
        max_length=200
    )
    author = models.IntegerField(
        'ID пользователя'
    )
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='reviews',
    #     verbose_name='Автор'
    # )
    score = models.IntegerField(
        'Оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={
            'validators': 'Оценка от 1 до 10!'
        }
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            )
        ]
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария к отзыву."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.CharField(
        'Текст комментария',
        max_length=200
    )
    author = models.IntegerField(
        'ID пользователя'
    )
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='comments',
    #     verbose_name='Автор'
    # )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
