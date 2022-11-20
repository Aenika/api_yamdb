from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import redirect
from django.http import HttpResponse


def is_admin(user):
    if not user.is_authenticated:
        return False
    # value = False
    # if user.role == 'adm':
    #     value = True
    # return value
