from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # quiz urls
    path('quiz/', views.quiz, name='quiz'),
    path('quiz_correct/', views.quiz_correct, name='quiz_correct'),
    path('quiz_incorrect/', views.quiz_incorrect, name='quiz_incorrect'),
    path('quiz_recap/', views.quiz_recap, name='quiz_recap')
]