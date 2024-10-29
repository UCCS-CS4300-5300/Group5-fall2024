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
    path('generate_quiz/', views.generate_quiz, name='generate_quiz'),
    path('next_question/', views.next_question, name = 'next_question'),
    
    # Path for word of the day
    path('word-of-the-day/', views.word_of_the_day, name="word_of_the_day"),
    
    # Path for registering
    path('register/', views.registerPage, name = 'registration-page'),

    # Path for logging in
    path('login/', views.loginPage, name='login-page'),

    # Path for logging out
    path('logout/', views.logout, name ='logout'),

    # path for selecting language
    path('set_language/', views.set_language, name='set_language'),

]