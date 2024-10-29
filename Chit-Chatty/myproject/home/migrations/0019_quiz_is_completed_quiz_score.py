# Generated by Django 5.1.1 on 2024-10-29 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_laststreakreset_member_hascompletedquiz_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='quiz',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]