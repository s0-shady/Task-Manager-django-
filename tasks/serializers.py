"""
TAS-2: Serializers for REST API
"""

from rest_framework import serializers
from .models import Task, Priority, Attachment


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ['id', 'name', 'weight']


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'filename', 'file', 'uploaded_at']


class TaskSerializer(serializers.ModelSerializer):
    priority = PrioritySerializer(read_only=True)
    priority_id = serializers.IntegerField(write_only=True, required=False)
    attachments = AttachmentSerializer(many=True, read_only=True)
    is_completed = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'content', 'date_added', 
            'completion_date', 'priority', 'priority_id',
            'attachments', 'is_completed'
        ]
