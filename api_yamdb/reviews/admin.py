from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('slug',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'year', 'category',)
    search_fields = ('name', 'year')
    list_filter = ('category', 'genre')


admin.site.register(Category, CategoryGenreAdmin)
admin.site.register(Genre, CategoryGenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Comment)
admin.site.register(Review)
