import hashlib
import time

from django.db import models


class TaskCategory(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=64
    )

    user_id = models.CharField(max_length=32, db_index=True)
    name = models.CharField(max_length=64)

    created_at = models.DateTimeField(auto_now_add=True)

    def compute_id(self) -> str:
        payload = f"{self.user_id}:{self.name}:{time.time_ns()}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:64]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.compute_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=64
    )

    user_id = models.CharField(max_length=32, db_index=True)
    category = models.ForeignKey(
        TaskCategory,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_at = models.DateTimeField(null=True)

    def compute_id(self) -> str:
        cat_id = self.category_id if self.category_id else "none"
        payload = f"{self.user_id}:{cat_id}:{self.content}:{time.time_ns()}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:64]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.compute_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.content[:20]}..."
