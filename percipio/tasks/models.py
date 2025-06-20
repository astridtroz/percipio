from django.db import models
from user.models import Provider, Contributor
from django.utils import timezone
from django.conf import settings


class Project(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=255)
    provider=models.ForeignKey(Provider, on_delete=models.CASCADE)
    created_at=models.DateTimeField(default=timezone.now)
    class Meta:
        unique_together=('title', 'provider')
    contributors= models.ManyToManyField(Contributor, related_name='contributed_projects')
    def __str__(self):
        return f"{self.title} - {self.id}"


class Task(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('completed', 'Completed'),
    ]
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=255)
    project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    provider= models.ForeignKey(Provider, on_delete=models.CASCADE)
    deadline = models.DateField(null=True, blank=True)
    created_at= models.DateTimeField( default=timezone.now)
    status= models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    contributor= models.ForeignKey(Contributor,on_delete=models.CASCADE, related_name='tasks', null=True)
    price=models.CharField(max_length=250, default=0)
    def __str__(self):
        return f"{self.title} - {self.status}"
    

class Application(models.Model):
    STATUS_CHOICES=[
        ('pending','Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    task=models.ForeignKey(Task, on_delete=models.CASCADE, related_name='applications')
    contributor= models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='application')
    message=models.TextField(blank=True, null=True)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    applied_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('contributor', 'task')
    
    def __str__(self):
        return f"{self.contributor.username} -> {self.task.title} ({self.status})"
    
    
class Submission(models.Model):
    task=models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    contributor= models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='submissions')
    project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name='submissions')
    submitted_at= models.DateTimeField(auto_now_add=True)
    workUrl=models.URLField()
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=300)

    def __str__(self):
        return self.title

