from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'pub_date', 'score', 'title')
    list_display_links = ('pk', 'author', 'pub_date')
    list_filter = ('author',)
    search_filter = ('title')
    empaty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'pub_date', 'review', 'title')
    list_display_links = ('pk', 'author', 'pub_date')
    list_filter = ('author',)
    search_filter = ('review')
    empaty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
