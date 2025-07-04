from rest_framework import serializers
from rest_framework import  schemas
from .models import Project, Task, Application, Submission

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'provider', 'deadline', 'created_at', 'status','price']
        read_only_fields = ['id','project', 'provider']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model= Project
        fields= ['id','title', 'description' ,'provider',  'created_at']
        read_only_fields=[ 'id', 'provider', 'created_at']

class ApplicationSerializer(serializers.ModelSerializer):
    contributor_username=serializers.CharField(source='contributor.username', read_only=True)
    task_title=serializers.CharField(source='task.title', read_only=True)

    class Meta:
        model= Application
        fields=['id', 'contributor', 'contributor_username', 'task', 'task_title', 'message', 'status', 'applied_at']
        read_only_fields=['id', 'applied_at', 'task', 'contributor']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Submission
        fields=['id', 'conributor', 'task', 'title', 'description', 'submitted_at', 'work_url']
        read_only_fields=['id', 'task']
