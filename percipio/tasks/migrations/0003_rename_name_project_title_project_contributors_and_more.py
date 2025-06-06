# Generated by Django 5.2 on 2025-06-01 20:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_created_at_task_deadline_and_more'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='project',
            name='contributors',
            field=models.ManyToManyField(related_name='contributors', to='user.contributor'),
        ),
        migrations.AddField(
            model_name='task',
            name='contributor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='contributor', to='user.contributor'),
        ),
        migrations.AddField(
            model_name='task',
            name='price',
            field=models.CharField(default=0, max_length=250),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('in_progress', 'In Progress'), ('submitted', 'Submitted'), ('completed', 'Completed')], default='open', max_length=20),
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('proposal', models.TextField(blank=True, null=True)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='tasks.task')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('workUrl', models.URLField()),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300)),
                ('contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='user.contributor')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='tasks.project')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='tasks.task')),
            ],
        ),
    ]
