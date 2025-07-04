# Generated by Django 5.2 on 2025-06-20 12:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_remove_task_contributors_task_contributor'),
        ('user', '0002_myuser_stripe_account_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='contributor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='user.contributor'),
        ),
    ]
