from django.urls import path, include
from .views import ProjectViewSet, TaskViewSet, ApplicationViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router= routers.DefaultRouter()

router.register(r'projects', ProjectViewSet, basename='projects')
#Nested under projects
projects_router= routers.NestedDefaultRouter(router, r'projects' , lookup='project')
projects_router.register(r'tasks', TaskViewSet, basename='project-tasks')

#Nested under tasks
tasks_router= routers.NestedDefaultRouter(projects_router, r'tasks', lookup='task')
tasks_router.register(r'applications', ApplicationViewSet, basename='task-application')


urlpatterns = router.urls + projects_router.urls + tasks_router.urls
