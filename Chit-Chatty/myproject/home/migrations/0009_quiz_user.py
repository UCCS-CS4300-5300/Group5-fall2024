# Generated by Django 5.1.1 on 2024-10-17 06:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_remove_question_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.member'),  # noqa: E501
        ),
    ]
