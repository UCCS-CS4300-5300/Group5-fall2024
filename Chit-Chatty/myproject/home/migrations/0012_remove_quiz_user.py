# Generated by Django 5.1.1 on 2024-10-25 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_remove_question_difficulty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='user',
        ),
    ]