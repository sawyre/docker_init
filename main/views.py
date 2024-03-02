from rest_framework import viewsets
from serializers import UserSerializer, TaskSerializer, TagSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = TaskSerializer.objects.select_related(
        "asignee", "created_by"
    ).prefetch_related("tags")
    serializer_class = TaskSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = TagSerializer.objects.order_by("id")
    serializer_class = TagSerializer
