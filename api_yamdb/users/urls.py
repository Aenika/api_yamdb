from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.v1.views import AdminUsersViewSet, MeUser, CheckCode, SendCode

v1_router = DefaultRouter()
v1_router.register('users', AdminUsersViewSet, basename='users')


urlpatterns = [
    path('v1/auth/token/', CheckCode.as_view(), name='token'),
    path('v1/auth/signup/', SendCode.as_view(), name='signup'),
    path('v1/users/me/', MeUser.as_view()),
    path('v1/', include(v1_router.urls))
]
