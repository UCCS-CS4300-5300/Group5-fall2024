# Generated by Django 5.1.1 on 2024-10-25 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_remove_quiz_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.member'),
        ),
    ]