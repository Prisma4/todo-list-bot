from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from tasks.models import Task, TaskCategory
from tasks.serializers import TaskSerializer, TaskCategorySerializer, TaskCategoryGetByNameSerializer, TaskGetSerializer
from todo_list.celery import app


class TasksModelViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related('category')
    permission_classes = (IsAdminUser,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id', 'category_id']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TaskSerializer
        return TaskGetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user_id = serializer.data.get('user_id')
        content = serializer.data.get('content')
        scheduled_at = serializer.data.get('scheduled_at')

        if user_id is not None and content is not None and scheduled_at is not None:
            app.send_task("bot.send_message", args=[user_id, content], eta=scheduled_at)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TaskCategoryModelViewSet(viewsets.ModelViewSet):
    queryset = TaskCategory.objects.all().prefetch_related('tasks')
    serializer_class = TaskCategorySerializer

    permission_classes = (IsAdminUser,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id']

    @action(methods=['POST'], detail=False, url_path='get_or_create_category_by_name')
    def get_or_create_by_name(self, request):
        serialized_data = TaskCategoryGetByNameSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

        name = serialized_data.validated_data['name']
        user_id = serialized_data.validated_data['user_id']

        obj, created = TaskCategory.objects.get_or_create(name=name, user_id=user_id)
        return Response({
            "id": obj.id,
            "name": obj.name,
            "created": created,
        }, status=status.HTTP_201_CREATED)
