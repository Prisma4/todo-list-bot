from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tasks.views import TasksModelViewSet, TaskCategoryModelViewSet

router = DefaultRouter()
router.register("tasks", TasksModelViewSet, basename="tasks")
router.register("category", TaskCategoryModelViewSet, basename="category")

urlpatterns = [
    path('', include(router.urls), name='tasks'),
]
