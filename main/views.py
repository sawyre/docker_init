import django_filters

from rest_framework import viewsets
from task_manager.permissions import IsAdminOrReadOnly
from .serializers import UserSerializer, TaskSerializer, TagSerializer
from .models import User, Tag, Task


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="icontains")
    role = django_filters.ChoiceFilter(choices=User.Roles.choices)

    class Meta:
        model = User
        fields = ("username", "role")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    status = django_filters.MultipleChoiceFilter(
        choices=Task.Statuses.choices, conjoined=False
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags__title",
        to_field_name="title",
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Task
        fields = ("title", "status", "tags")


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("assignee", "created_by").prefetch_related(
        "tags"
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permission_classes = [IsAdminOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
