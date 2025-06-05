from rest_framework import serializers
from .models import Project, Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'provider', 'deadline', 'created_at']
        read_only_fields = ['id', 'provider', 'created_at']


class ProjectSerializer(serializers.ModelSerializer):
    #tasks=TaskSerializer(many=True, read_only=True)
    class Meta:
        model= Project
        fields= ['id','title','project', 'description' ,'provider',  'created_at', 'status']
        read_only_fields=['id','status']
   


