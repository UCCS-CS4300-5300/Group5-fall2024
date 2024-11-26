# Generated by Django 5.1.1 on 2024-11-26 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_remove_quiz_is_next_quiz_correct_count_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='url',
        ),
        migrations.AddField(
            model_name='quiz',
            name='difficulty',
            field=models.CharField(default='Easy', max_length=20),
        ),
        migrations.AddField(
            model_name='quiz',
            name='length',
            field=models.IntegerField(default=5),
        ),
    ]
