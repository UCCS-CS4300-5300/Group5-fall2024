from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Quiz, Member
from .forms import CreateUserForm
from .decorators import unauthenticatedUser

def index(request):
    # Fetch the quiz that is marked as the next quiz
    next_quiz = Quiz.objects.filter(is_next=True).first()
    
    context = {
        'quiz_title': next_quiz.title if next_quiz else 'Nothing!',
        'quiz_description': next_quiz.description if next_quiz else 'Check back later for new content.',
        'quiz_url': next_quiz.url if next_quiz else '#',
    }
    return render(request, 'home/index.html', context)

'''
View for user registration
Takes the information from the form to make a 'Member'
'''
@unauthenticatedUser
def registerPage(request):
    # Create registration fields
    form = CreateUserForm()
    
    if request.method =='POST':
        # Fill form with submission information
        form = CreateUserForm(request.POST)
        if form.is_valid():

            # Save form to database and store the instance in variable
            user = form.save()

            # Get the all fields from the form
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')

            # Create the member object and associate with user
            Member.objects.create(
                user=user,
                userName = username,
                firstName = first_name,
                lastName = last_name,
                email = email,
            )

            # Create success message 
            messages.success(request, 'Account was created for ' + username)
            return redirect('login-page')

    context = {'form': form}
    return render(request, 'authentication/register.html', context)

'''
View for logging in
'''
@unauthenticatedUser
def loginPage(request):
    # If request is post, then try to log in user. Otherwise, send form type
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('index')  
    else:
        form = AuthenticationForm()
    
    return render(request, 'authentication/login.html', {'form': form})

'''
View for logging out
Redirects user back to the login-page no matter what (because returning render after logging out isn't executing for some reason)
'''
@login_required(login_url='login-page')
def logout(request):
    auth_logout(request) 
    return render(request, 'home/index.html')

# Quiz Views
def quiz(request):
    # Fetch the quiz marked as the next one
    next_quiz = Quiz.objects.filter(is_next=True).first()
    
    if next_quiz:
        # Get the first question from this quiz
        first_question = next_quiz.questions.first()
        context = {
            'quiz': next_quiz,
            'question': first_question
        }
    else:
        # If no next quiz is found, you could display a message
        context = {'error': "No quiz available."}
    
    return render(request, 'home/quiz_question.html', context)

# Quiz Check view
def quiz_check_answer(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        user_answer = request.POST.get('user_answer').strip().lower()

        question = get_object_or_404(Question, id=question_id)
        correct_answer = question.correct_answer.strip().lower()

        # Store question, user's answer, and correct answer in the session
        request.session['question'] = question.translation_question
        request.session['user_answer'] = user_answer
        request.session['correct_answer'] = correct_answer

        if user_answer == correct_answer:
            return redirect('quiz_correct')
        else:
            return redirect('quiz_incorrect')

    return redirect('quiz')


# Quiz Correct
def quiz_correct(request):
    # Assuming the question and answer have been saved in the session during quiz_check_answer
    question = request.session.get('question')
    user_answer = request.session.get('user_answer')

    context = {
        'question': question,
        'user_answer': user_answer,
        'feedback': "Great job!"
    }
    return render(request, 'home/quiz_correct.html', context)


# Quiz Incorrect View
def quiz_incorrect(request):
    context = {
        'message': "You'll get it next time!"
    }
    return render(request, 'home/quiz_incorrect.html', context)

# Quiz Recap
def quiz_recap(request):
    return render(request, 'home/quiz_recap.html')