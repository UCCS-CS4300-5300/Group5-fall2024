# Generated by Django 5.1.1 on 2024-10-17 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_quiz_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='questions',
            field=models.ManyToManyField(to='home.question'),
        ),
    ]
