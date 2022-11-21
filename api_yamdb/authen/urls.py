from django.urls import path
from rest_framework.authtoken import views

from .views import CheckCode, SendCode

urlpatterns = [
    path('token/', CheckCode.as_view()),
    path('signup/', SendCode.as_view(), name='signup'),

]
