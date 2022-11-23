import random

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, **extra_fields):
        u = self.model(email=email, username=username, **extra_fields)
        u.save()
        CodeEmail.objects.create(email=email, username=username,
                                 confirmation_code=''.join(
                                     [str(random.randint(0, 10)) for i in range(6)]))

        return u

    def create_superuser(self, email, username, role='admin', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email=email, username=username, role=role)


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('user', 'User')
    )
    role = models.CharField(choices=USER_TYPE_CHOICES,
                            max_length=10,
                            default='user')
    bio = models.TextField('Биография',
                           blank=True,
                           null=True)
    email = models.EmailField(max_length=254,
                              blank=False,
                              null=False,
                              unique=True)
    objects = CustomUserManager()


class CodeEmail(models.Model):
    confirmation_code = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=150)
    username = models.CharField(max_length=150)
