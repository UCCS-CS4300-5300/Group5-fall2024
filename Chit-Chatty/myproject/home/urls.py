from django.urls import path, include
from . import views

urlpatterns = [
    # Default path (Home)
    path('', views.index, name='index'),

    # Paths for the quiz
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/quiz_correct/', views.quiz_correct, name='quiz_correct'),
    path('quiz/quiz_incorrect/', views.quiz_incorrect, name='quiz_incorrect'),
    path('quiz/quiz_recap/', views.quiz_recap, name='quiz_recap'),
    path('quiz/check_answer/', views.quiz_check_answer, name='quiz_check_answer'),
    path('generate_quiz/', views.generate_quiz, name='generate_quiz')
    
    # Path for registering
    path('register/', views.registerPage, name = 'registration-page'),

    # Path for logging in
    path('login/', views.loginPage, name='login-page'),

    # Path for logging out
    path('logout/', views.logout, name ='logout'),
]