from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants import (
    CHARS_FOR_CODE, CHARS_FOR_EMAIL, CHARS_FOR_PASSWORD, CHARS_FOR_ROLE
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, **extra_fields):
        u = self.model(email=email, username=username, **extra_fields)
        u.save()
        return u

    def create_superuser(self, email, username, role='admin', **extra_fields):
        return self.create_user(email=email,
                                username=username,
                                role=role,
                                confirmation_code='123456',
                                is_superuser=True)


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('user', 'User')
    )
    role = models.CharField(choices=USER_TYPE_CHOICES,
                            max_length=CHARS_FOR_ROLE,
                            default='user')
    bio = models.TextField('Биография',
                           blank=True,
                           null=True)
    email = models.EmailField(max_length=CHARS_FOR_EMAIL,
                              blank=False,
                              null=False,
                              unique=True)
    password = models.CharField(
        max_length=CHARS_FOR_PASSWORD,
        blank=True,
        null=True
    )
    confirmation_code = models.CharField(
        max_length=CHARS_FOR_CODE,
        blank=True,
        null=True
    )
    objects = CustomUserManager()
