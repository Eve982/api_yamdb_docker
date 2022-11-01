from django.db import models
from .validators import validate_year


class Category(models.Model):
    slug = models.SlugField(
        verbose_name='Slug категории',
        max_length=50,
        unique=True,
    )
    title = models.CharField(
        verbose_name='Название категории',
        max_length=250,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Genre(models.Model):
    slug = models.SlugField(
        verbose_name='Slug жанра',
        max_length=50,
        unique=True,
    )
    title = models.CharField(
        verbose_name='Название жанра',
        max_length=250,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг произведения',
        null=True,
        default=None,
    )
    title = models.CharField(
        verbose_name='Название произведения',
        max_length=200,
    )
    year = models.DateTimeField(
        blank=True,
        verbose_name='Год создания произведения',
        format="%Y",
        validators=[validate_year, ]
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['title']
