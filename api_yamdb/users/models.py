from core.constants import (
    ADMIN,
    MODERATOR,
    REG_USER
)
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import (
    CHARS_FOR_CODE,
    CHARS_FOR_EMAIL,
    CHARS_FOR_PASSWORD,
    CHARS_FOR_ROLE,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, **extra_fields):
        u = self.model(email=email, username=username, **extra_fields)
        u.save()
        return u

    def create_superuser(self, email, username, role=ADMIN, **extra_fields):
        return self.create_user(email=email,
                                username=username,
                                role=role,
                                confirmation_code='123456',
                                is_superuser=True)


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (ADMIN, 'Admin'),
        (MODERATOR, 'Moderator'),
        (REG_USER, 'User')
    )
    role = models.CharField(choices=USER_TYPE_CHOICES,
                            max_length=CHARS_FOR_ROLE,
                            default=REG_USER,
                            verbose_name='статус')
    bio = models.TextField(blank=True,
                           null=True,
                           verbose_name='Биография')
    email = models.EmailField(max_length=CHARS_FOR_EMAIL,
                              blank=False,
                              null=False,
                              unique=True,
                              verbose_name='Почта')
    password = models.CharField(
        max_length=CHARS_FOR_PASSWORD,
        blank=True,
        null=True,
        verbose_name='Пароль'
    )
    confirmation_code = models.CharField(
        max_length=CHARS_FOR_CODE,
        blank=True,
        null=True,
        verbose_name='Код подтврждения'
    )
    objects = CustomUserManager()

    @property
    def is_admin(self):
        return self.role == ADMIN
    @property
    def is_moderator(self):
        return self.role == MODERATOR
