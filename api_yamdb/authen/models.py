from django.db import models


class CodeEmail(models.Model):
    code = models.CharField(max_length=6, blank=True)
    email = models.EmailField(max_length=150)
    username = models.CharField(max_length=150)
