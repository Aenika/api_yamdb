from django.contrib.auth.models import AbstractUser
from django.db import models


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
                           blank=True)
    email = models.EmailField(max_length=254,
                              blank=False,
                              unique=True)
