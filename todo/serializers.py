from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'status', 'created_at',
            'due_date', 'is_overdue', 'user']
        read_only_fields = ['created_at', 'is_overdue']

    def get_is_overdue(self, obj):
        return obj.is_overdue()