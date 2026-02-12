from django.contrib import admin

from tasks.models import Task, TaskCategory

admin.site.register(Task)
admin.site.register(TaskCategory)
