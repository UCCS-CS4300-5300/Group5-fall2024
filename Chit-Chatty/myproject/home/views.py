from django.shortcuts import render
from django.http import HttpResponse
from .models import Quiz

def index(request):
    # Fetch the quiz that is marked as the next quiz
    next_quiz = Quiz.objects.filter(is_next=True).first()
    
    context = {
        'quiz_title': next_quiz.title if next_quiz else 'Nothing!',
        'quiz_description': next_quiz.description if next_quiz else 'Check back later for new content.',
        'quiz_url': next_quiz.url if next_quiz else '#',
    }
    return render(request, 'home/index.html', context)

# quiz views
def quiz(request):
    return render(request, 'home/quiz_question.html')

def quiz_correct(request):
    return render(request, 'home/quiz_correct.html')

def quiz_incorrect(request):
    return render(request, 'home/quiz_incorrect.html')

def quiz_recap(request):
    return render(request, 'home/quiz_recap.html')