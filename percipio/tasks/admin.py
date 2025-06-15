from django.contrib import admin
from .models import Project, Task, Application, Submission
# Register your models here.

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Application)
admin.site.register(Submission)