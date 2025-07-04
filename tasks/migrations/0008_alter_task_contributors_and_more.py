# Generated by Django 5.2 on 2025-06-18 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_remove_application_proposal_and_more'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='contributors',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='user.contributor'),
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together={('title', 'provider')},
        ),
    ]
