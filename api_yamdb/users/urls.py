from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdminUsersViewSet, MeUser, CheckCode, SendCode

v1_router = DefaultRouter()
v1_router.register('users', AdminUsersViewSet, basename='users')


urlpatterns = [
    path('auth/token/', CheckCode.as_view(), name='token'),
    path('auth/signup/', SendCode.as_view(), name='signup'),
    path('users/me/', MeUser.as_view()),
    path('', include(v1_router.urls))
]
