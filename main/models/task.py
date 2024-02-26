from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .user import User
from .tag import Tag
from main.exceptions import UnavailableStatusChange

from datetime import datetime


class Task(models.Model):
    class Statuses(models.TextChoices):
        NEW_TASK = "new_task"
        IN_DEVELOPMENT = "in_development"
        IN_QA = "in_qa"
        IN_CODE_REVIEW = "in_code_review"
        READY_FOR_RELEASE = "ready_for_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    title = models.CharField(max_length=50)
    description = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True)
    status = models.CharField(default=Statuses.NEW_TASK, choices=Statuses.choices)
    priority = models.PositiveIntegerField(
        default=1, validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author"
    )
    assignee = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="assignee"
    )
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ["-priority"]

    def change_status(self, new_status: Statuses) -> None:
        available_status_changes = {
            self.Statuses.NEW_TASK: {
                self.Statuses.IN_DEVELOPMENT,
                self.Statuses.ARCHIVED,
            },
            self.Statuses.IN_DEVELOPMENT: [self.Statuses.IN_QA],
            self.Statuses.IN_QA: {
                self.Statuses.IN_DEVELOPMENT,
                self.Statuses.IN_CODE_REVIEW,
            },
            self.Statuses.IN_CODE_REVIEW: {
                self.Statuses.READY_FOR_RELEASE,
                self.Statuses.IN_DEVELOPMENT,
            },
            self.Statuses.READY_FOR_RELEASE: {self.Statuses.REALESED},
            self.Statuses.REALESED: {self.Statuses.ARCHIVED},
        }

        if (
            self.status in available_status_changes
            and new_status in available_status_changes[self.status]
        ):
            self.status = new_status
            self.save()
        else:
            raise UnavailableStatusChange()
