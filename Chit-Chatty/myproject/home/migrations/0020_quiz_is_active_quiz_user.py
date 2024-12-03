# Generated by Django 5.1.1 on 2024-11-12 22:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_quiz_is_completed_quiz_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.member'),  # noqa: E501
        ),
    ]
