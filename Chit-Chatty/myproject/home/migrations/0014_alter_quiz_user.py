# Generated by Django 5.1.1 on 2024-10-25 17:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_quiz_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.member'),
        ),
    ]
