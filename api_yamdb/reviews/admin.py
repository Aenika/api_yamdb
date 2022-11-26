from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'pub_date', 'score', 'title')
    list_display_links = ('pk', 'author', 'pub_date')
    list_filter = ('author',)
    search_filter = ('title',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'pub_date', 'review', 'title')
    list_display_links = ('pk', 'author', 'pub_date')
    list_filter = ('author',)
    search_filter = ('review',)
    empty_value_display = '-пусто-'


class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('slug',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'year', 'category',)
    search_fields = ('name', 'year')
    list_filter = ('category',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryGenreAdmin)
admin.site.register(Genre, CategoryGenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
