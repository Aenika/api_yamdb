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
                           blank=True,
                           null=True)
    email = models.EmailField(max_length=254,
                              blank=False,
                              null=True,
                              unique=True)

    def create_superuser(self, email, username, first_name='super', second_name='user',
                         bio='superbio', role='admin'):
        u = self.create_superuser(email, username, first_name, second_name,
                                  bio, role)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class CodeEmail(models.Model):
    confirmation_code = models.CharField(max_length=6, blank=True)
    email = models.EmailField(max_length=150)
    username = models.CharField(max_length=150)
