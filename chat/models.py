from django.db import models
from tasks.models import Project
from user.models import MyUser

class PrivateChatMessage(models.Model):
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='sent_private_messages')
    receiver = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='received_private_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class ProjectGroupChatMessage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
