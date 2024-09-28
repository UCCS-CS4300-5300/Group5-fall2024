from django.db import models

# Create your models here.


# models.py
from django.db import models


# Quiz model
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.CharField(max_length=100)
    # Flag to identify the next quiz
    is_next = models.BooleanField(default=False)  

    def __str__(self):
        return self.title
