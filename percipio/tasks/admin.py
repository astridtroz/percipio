from django.contrib import admin
from .models import Project, Task, Application
# Register your models here.

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Application)