from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from todo_list import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("tasks/", include("tasks.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
