from django.contrib.auth.models import AbstractUser
from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=50)
