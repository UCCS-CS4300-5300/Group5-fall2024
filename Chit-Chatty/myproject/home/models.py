from django.db import models
from django.contrib.auth.models import User
# from django.utils.translation import gettext_lazy as _


# Create your models here.

# Quiz model
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    length = models.IntegerField(default=5)
    difficulty = models.CharField(max_length=20, default="Easy")

    # Link quiz to user (optional, uncomment to use)
    user = models.ForeignKey('Member', on_delete=models.CASCADE,
                             null=True, blank=True)

    # Holds all questions in the model
    questions = models.ManyToManyField('Question',
                                       related_name='quiz_questions')

    # For quiz tracking
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    score = models.IntegerField(null=True, blank=True)
    curr_question = models.ForeignKey(
                                      'Question',
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True)
    correct_count = models.IntegerField(default=0)
    incorrect_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


# Class model
class Question(models.Model):
    # Phrase in the source language
    translation_question = models.CharField(max_length=300)
    correct_answer = models.CharField(max_length=300)
    source_language = models.CharField(max_length=50, default="Spanish")
    target_language = models.CharField(max_length=50, default="English")

    def __str__(self):
        return self.translation_question


# User model
class Member(models.Model):
    # Fields that makes a user unique
    userName = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50, default="")
    lastName = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=50, default="")
    dateJoined = models.DateField(auto_now_add=True)

    # Streak information
    streakCount = models.IntegerField(default=0)
    longestStreak = models.IntegerField(default=0)
    hasCompletedQuiz = models.BooleanField(default=False)

    # One to one relationship with user
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.userName


# Tracks last reset for streaks (since our servers aren't always running)
class LastStreakReset(models.Model):
    lastReset = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Last streak reset was at: {self.lastReset}"
