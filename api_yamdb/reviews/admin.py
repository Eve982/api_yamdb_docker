from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
    )
    search_fields = ('title', 'author', 'pub_date',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
