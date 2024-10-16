from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Quiz model
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.CharField(max_length=100)
    # Flag to identify the next quiz
    is_next = models.BooleanField(default=False)  

    def __str__(self):
        return self.title

# Question Model
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    translation_question = models.CharField(max_length=300)
    correct_answer = models.CharField(max_length=300)  
    # Optional feedback if wrong
    feedback = models.TextField(null=True, blank=True)  

    def __str__(self):
        return self.translation_question


# User model
class Member(models.Model):

    # Fields that makes a user unique
    userName = models.CharField(max_length= 50)
    firstName = models.CharField(max_length= 50, default="")
    lastName = models.CharField(max_length= 50, default="")
    email = models.CharField(max_length= 50, default="")

    # One to one relationship with user
    user = models.OneToOneField(User, null= True, on_delete=models.CASCADE)

    def __str__(self):
        return self.userName