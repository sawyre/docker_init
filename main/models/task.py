from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from .user import User
from .tag import Tag


class Task(models.Model):
    class Statuses(models.TextChoices):
        NEW_TASK = "new_task"
        IN_DEVELOPMENT = "in_development"
        IN_QA = "in_qa"
        IN_CODE_REVIEW = "in_code_review"
        READY_FOR_RELEASE = "ready_for_release"
        REALESED = "released"
        ARCHIVED = "archived"

    title = models.CharField(max_length=50)
    description = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True)
    status = models.DateField(default=Statuses.NEW_TASK, choices=Statuses.choices)
    priority = models.PositiveIntegerField(
        default=1, validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author"
    )
    executor = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="executor"
    )
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ["-priority"]
