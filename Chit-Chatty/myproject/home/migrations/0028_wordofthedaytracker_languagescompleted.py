# Generated by Django 5.1.1 on 2024-12-09 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_rename_wordofthedaychecker_wordofthedaytracker'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordofthedaytracker',
            name='languagesCompleted',
            field=models.TextField(blank=True, default=''),
        ),
    ]
