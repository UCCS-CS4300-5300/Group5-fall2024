# Generated by Django 5.1.1 on 2024-10-28 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_rename_currentstreakcount_member_streakcount'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreakResetLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_run_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
