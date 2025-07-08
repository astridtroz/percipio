from django.urls import path, include
from .views import ProjectViewSet, TaskViewSet, ApplicationViewSet, SubmissionViewSet, ContributorTasksViewset, ContributorSubmissions
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router= routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'mytasks', ContributorTasksViewset, basename='mytasks')

#Nested under projects
projects_router= routers.NestedDefaultRouter(router, r'projects' , lookup='project')
projects_router.register(r'tasks', TaskViewSet, basename='project-tasks')

#Nested under tasks
tasks_router= routers.NestedDefaultRouter(projects_router, r'tasks', lookup='task')
tasks_router.register(r'applications', ApplicationViewSet, basename='task-applications')
tasks_router.register(r'submissions',  SubmissionViewSet, basename='task-submissions')

#nested under mytasks
mytask_router= routers.NestedDefaultRouter(router, r'mytasks', lookup='mytask')
mytask_router.register(r'mysubmissions', ContributorSubmissions, basename='mytask-submission')



urlpatterns = router.urls  + mytask_router.urls+ projects_router.urls + tasks_router.urls 
