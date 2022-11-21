from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AdminUsersViewSet, MeUser

v1_router = DefaultRouter()
v1_router.register('users', AdminUsersViewSet, basename='users')


urlpatterns = [
    path('users/me/', MeUser.as_view()),
    path('', include(v1_router.urls))

]
