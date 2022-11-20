from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AdminUsersViewSet, MeUser

user_router = DefaultRouter()
user_router.register('users', AdminUsersViewSet, basename='users')


urlpatterns = [
    path('users/me/', MeUser.as_view()),
    path('', include(user_router.urls))

]
