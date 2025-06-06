# Generated by Django 5.2 on 2025-06-06 15:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_project_contributors'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='contributor',
        ),
        migrations.AddField(
            model_name='application',
            name='contributor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application', to='user.contributor'),
        ),
        migrations.AddField(
            model_name='task',
            name='contributors',
            field=models.ManyToManyField(related_name='tasks', to='user.contributor'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='contributor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='user.contributor'),
        ),
    ]
