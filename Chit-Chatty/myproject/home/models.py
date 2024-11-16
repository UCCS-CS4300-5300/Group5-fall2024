from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.

# Quiz model
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.CharField(max_length=100)
    
    # Flag to identify the next quiz
    is_next = models.BooleanField(default=False)  
    
    # Link quiz to user (optional, uncomment to use)
    user = models.ForeignKey('Member', on_delete=models.CASCADE, null=True, blank=True)
    
    # Holds all questions in the model
    questions = models.ManyToManyField('Question')

    # For quiz tracking
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    def set_next_quiz(self):
        """
        Mark this quiz as the next quiz and unset 'is_next' for all other quizzes for the same user.
        """
        if self.user:
            # Ensure only one quiz is marked as is_next for the user
            Quiz.objects.filter(user=self.user).update(is_next=False)
        self.is_next = True
        self.save()

    @classmethod
    def update_next_quiz(cls, user):
        """
        Update the next quiz dynamically for a given user.
        """
        # Find the first active, incomplete quiz for the user
        next_quiz = cls.objects.filter(user=user, is_active=True, is_completed=False).order_by('id').first()
        
        # Update the is_next flag
        if next_quiz:
            cls.objects.filter(user=user).update(is_next=False)  # Unset all other quizzes
            next_quiz.is_next = True
            next_quiz.save()
        else:
            # If no quiz is available, unset all is_next flags
            cls.objects.filter(user=user).update(is_next=False)

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
    userName = models.CharField(max_length= 50)
    firstName = models.CharField(max_length= 50, default="")
    lastName = models.CharField(max_length= 50, default="")
    email = models.CharField(max_length= 50, default="")
    dateJoined = models.DateField(auto_now_add=True)

    # Streak information 
    streakCount = models.IntegerField(default = 0)
    longestStreak = models.IntegerField(default = 0)
    hasCompletedQuiz = models.BooleanField(default = False)

    # One to one relationship with user
    user = models.OneToOneField(User, null= True, on_delete=models.CASCADE)

    def __str__(self):
        return self.userName

# Tracks last reset for streaks (since our servers aren't always running)
class LastStreakReset(models.Model):
    lastReset = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"Last streak reset was at: {self.lastReset}"