from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from .models import Project, Task, Application, Submission, Contributor
from .serializers import ProjectSerializer, TaskSerializer, ApplicationSerializer, SubmissionSerializer
from user.models import Provider
from django.shortcuts import get_object_or_404

class CanCreateProjectPermission(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'provider')

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    #permission_classes = [CanCreateProjectPermission]
    def perform_create(self, serializer):
        provider = get_object_or_404( Provider, user_obj=self.request.user)
        title = serializer.validated_data.get('title')
        if Project.objects.filter(title=title, provider=provider).exists():
            raise serializers.ValidationError("Project with this title already exists for this provider.")
        if provider:
            serializer.save(provider=provider)

def usertype(request):
    if request.user__user_obj in Provider.objects.all():
        return "provider"
    else:
        return "contributor"



class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
            return Task.objects.filter(
                project__id=self.kwargs['project_pk'],
            )


    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs['project_pk'])
        
        if project.provider.user_obj != self.request.user:
            raise PermissionDenied("You are not the owner of this project.")

        
        title = serializer.validated_data['title']
        if Task.objects.filter(project=project, title=title).exists():
            raise serializers.ValidationError("This task already exists for the given project.")
        
       
        serializer.save(project=project, provider=project.provider)

    def update(self, request, *args, **kwargs):
        instance= self.get_object()
        if instance.project.provider.user_obj!=request.user:
            raise PermissionDenied("You are not allowed to update this task.")
        status_to_set=request.data.get('status')
        if status_to_set not in ['open', 'in_progress','submitted','completed']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        instance.status = status_to_set
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    



class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(
            task__id=self.kwargs['task_pk'],
            task__project__id=self.kwargs['project_pk'],
            #task__project__provider__user_obj=self.request.user
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.task.project.provider.user_obj != request.user:
            raise PermissionDenied("You are not allowed to update this application.")

        status_to_set = request.data.get('status')
        if status_to_set not in ['approved', 'rejected']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        instance.status = status_to_set

        if instance.status == 'approved':
            instance.task.contributor = instance.contributor
            instance.task.status='in_progress'
            instance.task.save()

        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        task= Task.objects.get(id=self.kwargs['task_pk'])
        contributor=Contributor.objects.get(user_obj=self.request.user)
        if  task.project.provider == contributor:
            raise PermissionDenied("Provider not allowed to apply")
        serializer.save(task=task, contributor=contributor)

    def create(self, request, *args, **kwargs):

        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        application=serializer.instance
        full_data=self.get_serializer(application).data
        return Response(full_data, status=status.HTTP_201_CREATED)
    
              

class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class= SubmissionSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Submission.objects.filter(
            task__id= self.kwargs['task_pk'],
            task__project__id= self.kwargs['project_pk'],
            task__project__provider__user_obj=self.request.user
        )
    
    


class ContributorTasksViewset(viewsets.ModelViewSet):
    serializer_class= TaskSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            contributor__user_obj=self.request.user
        )

class ContributorSubmissions(viewsets.ModelViewSet):
    serializer_class= SubmissionSerializer
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        task_id= self.kwargs.get('mytask_pk')
        return Submission.objects.filter(
            contributor__user_obj=self.request.user,
            task= get_object_or_404(Task, id=task_id)
        )
    def perform_create(self, serializer):
        contributor= get_object_or_404(Contributor, user_obj=self.request.user)
        task_id= self.kwargs.get('mytask_pk')
        print(task_id)
        task= get_object_or_404(Task, id=task_id)
        project= task.project
        task.status="submitted"
        task.save()
        serializer.save(contributor=contributor, task_id=task_id, project=project )
        