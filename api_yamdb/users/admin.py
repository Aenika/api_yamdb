from django.contrib import admin

from .models import User


# class UserAdmin(admin.ModelAdmin):
#    list_display = ('username', 'email', 'role', 'bio')
#    search_fields = ('username',)
#    list_filter = ('role',)


admin.site.register(User)
