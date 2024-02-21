from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        DEVELOPER = "developer"
        MANAGER = "manager"
        ADMIN = "admin"

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(
        max_length=255, default=Roles.DEVELOPER, choices=Roles.choices
    )
    mail = models.CharField(null=True, validators=[EmailValidator])
