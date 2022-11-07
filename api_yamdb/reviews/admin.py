from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Comment, Genre, Review, Title, User


# admin.site.register(User, UserAdmin)

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
    list_editable = ['role']
    # actions = ['is_user', 'is_admin', 'is_moderator']
    list_filter = ('username', )
    search_fields = ('username', 'role',)

    # @admin.action(description='Пользователь')
    # def is_user(self, request, queryset):
    #     queryset.update(role='USER')

    # @admin.action(description='Администратор')
    # def is_admin(self, request, queryset):
    #     queryset.update(role='ADMIN')

    # @admin.action(description='Модератор')
    # def is_moderator(modeladmin, request, queryset):
    #     queryset.update(role='MODERATOR')


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


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year',
        'description', 'category',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
