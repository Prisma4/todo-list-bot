from rest_framework import serializers

from tasks.models import Task, TaskCategory


class TaskCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = '__all__'
        read_only_fields = ('id',)


class TaskGetSerializer(serializers.ModelSerializer):
    category = TaskCategorySerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id',)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id',)


class TaskCategoryGetByNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = (
            "user_id",
            "name",
        )
