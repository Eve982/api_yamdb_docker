from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка Пользователей."""

    list_display = (
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )
    list_editable = ('role',)
    list_filter = ('username', )
    search_fields = ('username', 'role',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'title', 'text',
        'author', 'score', 'pub_date',
    )
    search_fields = ('title', 'author', 'pub_date')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'review', 'text',
        'author', 'pub_date',
    )
    search_fields = ('review', 'author', 'pub_date')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class GenreTitleInline(admin.TabularInline):
    model = Title.genre.through


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year',
        'description', 'category',
    )
    search_fields = ('name',)
    list_filter = ('year', 'category', 'genre',)
    list_editable = ('category',)
    empty_value_display = '-пусто-'
    inlines = [GenreTitleInline]
