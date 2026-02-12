from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from tasks.models import Task, TaskCategory
from tasks.serializers import TaskSerializer, TaskCategorySerializer


class TasksModelViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id', 'category_id']


class TaskCategoryModelViewSet(viewsets.ModelViewSet):
    queryset = TaskCategory.objects.all()
    serializer_class = TaskCategorySerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id']
