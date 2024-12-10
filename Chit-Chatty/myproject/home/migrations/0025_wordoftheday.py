# Generated by Django 5.1.1 on 2024-12-09 23:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_remove_quiz_url_quiz_difficulty_quiz_length'),  # noqa: E501
    ]

    operations = [
        migrations.CreateModel(
            name='WordOfTheDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # noqa: E501
                ('languagesGenerated', models.TextField(blank=True, default='')),  # noqa: E501
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.member')),  # noqa: E501
            ],
        ),
    ]
