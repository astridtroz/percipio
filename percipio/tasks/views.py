from django.shortcuts import render
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import ProjectSerializer, TaskSerializer
from .models import Project
from rest_framework import status, viewsets, permissions
from user.models import Provider
# Create your views here.

class Cancreateprojectpermission(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'provider')

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [Cancreateprojectpermission]

    def perform_create(self, serializer):
        provider=Provider.objects.get(user_obj=self.request.user)
        title=serializer.validated_data.get('title')
        
        if Project.objects.filter(title=title , provider=provider).exists():
            raise  serializers.ValidationError("Project with this title has been already created by the current Provider")
        
        serializer.save(provider=provider)



