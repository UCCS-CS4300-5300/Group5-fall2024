from django.urls import path, include
from . import views

urlpatterns = [
    # Default path (Home)
    path('', views.index, name='index'),

    # quiz urls
    path('quiz/', views.quiz, name='quiz'),,

    # Path for registering
    path('register/', views.registerPage, name = 'registration-page'),

    # Path for logging in
    path('login/', views.loginPage, name='login-page'),

    # Path for logging out
    path('logout/', views.logout, name ='logout'),
    path('quiz_correct/', views.quiz_correct, name='quiz_correct'),
    path('quiz_incorrect/', views.quiz_incorrect, name='quiz_incorrect'),
    path('quiz_recap/', views.quiz_recap, name='quiz_recap')
]