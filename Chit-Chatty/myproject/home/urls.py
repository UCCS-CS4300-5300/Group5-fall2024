from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from . import views
from .views import MemberViewSet, QuizViewSet, QuestionViewSet

# Used to manage the API routes
router = DefaultRouter()

# Register all the viewsets to manage API endpoints
router.register(r'members', MemberViewSet, basename = 'members')
router.register(r'quizzes', QuizViewSet, basename = 'quizzes')
router.register(r'questions', QuestionViewSet, basename = 'questions')

urlpatterns = [
    # Default path (Home)
    path('', views.index, name='index'),

    #Used to handle all API related stuff
    path('api/', include(router.urls)),
    
    # Paths for the quiz
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/quiz_correct/', views.quiz_correct, name='quiz_correct'),
    path('quiz/quiz_incorrect/', views.quiz_incorrect, name='quiz_incorrect'),
    path('quiz/quiz_recap/', views.quiz_recap, name='quiz_recap'),
    path('quiz/check_answer/', views.quiz_check_answer, name='quiz_check_answer'),
    path('generate_quiz/', views.generate_quiz, name='generate_quiz'),
    path('next_question/', views.next_question, name = 'next_question'),
    path('quiz_start/', views.quiz_start, name = 'quiz_start'),
    path('continue_quiz/', views.continue_quiz, name='continue_quiz'),
    path('exit_quiz/', views.exit_quiz, name='exit_quiz'),
    
    # Path for word of the day
    path('word-of-the-day/', views.word_of_the_day, name='word_of_the_day'),

    # Path for daily lesson
    path('daily-lesson/', views.daily_lesson, name='daily_lesson'),
    
    # Path for registering
    path('register/', views.registerPage, name = 'registration-page'),

    # Path for logging in
    path('login/', views.loginPage, name='login-page'),

    # Path for logging out
    path('logout/', views.logout, name ='logout'),

    # Path for account details
    path('account-details/<int:userID>', views.accountPage, name='account_details'),

    # Path for editing account details
    path('update_account_details/', views.update_account_details, name='update_account_details'),

    # path for selecting language
    path('set_language/', views.set_language, name='set_language'),

]