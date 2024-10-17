from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Quiz, Member, Question
from .forms import CreateUserForm
from .decorators import unauthenticatedUser
import random

# Home Page View
def index(request):
    # Fetch the quiz that is marked as the next quiz
    next_quiz = Quiz.objects.filter(is_next=True).first()
    
    context = {
        'quiz_available': bool(next_quiz),  # Boolean flag to indicate if a quiz is available
        'quiz_title': next_quiz.title if next_quiz else 'No Quiz Loaded!',
        'quiz_description': next_quiz.description if next_quiz else 'Check back later for new content.',
        
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
    # Reset the session when starting a new quiz
    request.session['correct_count'] = 0
    request.session['incorrect_count'] = 0
    request.session['question_id'] = 1

    # Fetch the next quiz and the first question
    next_quiz = Quiz.objects.filter(is_next=True).first()

    if next_quiz:
        first_question = next_quiz.questions.first()

        # Ensure there is at least one question in the quiz
        if not first_question:
            context = {
                'quiz': next_quiz,
                'error': "No questions available for this quiz."
            }
            
        else:
            request.session['question_id'] = first_question.id

            # Set the question number for the first question (it will always be 1)
            question_number = 1

            context = {
                'quiz': next_quiz,
                'question': first_question,
                'question_number': question_number  # Include question number in context
            }
    else:
        context = {'error': "No quiz available."}

    return render(request, 'quiz/quiz_question.html', context)


# Generate Quiz view
@login_required
def generate_quiz(request):
    # Check for POST request with selected difficulty
    print(request)
    if request.method == 'POST':
        difficulty = request.POST.get('difficulty')

        # Ensure difficulty is received
        if difficulty:
            #Retrieve 10 random questions based on the selected difficulty
            questions = Question.objects.filter(difficulty=difficulty).order_by('?')[:10]

            # Quiz creation
            if questions.exists():
                # Create user instance
                member = get_object_or_404(Member, user=request.user)

                # Create a new quiz for the user 
                quiz = Quiz.objects.create(user=member, is_next=True)
                #print(request)
                quiz.questions.set(questions)

                # Mark the quiz as the "Next" quiz for the user
                Quiz.objects.filter(user=member).update(is_next=False)
                quiz.is_next = True
                quiz.save()
                request.session['quiz_id'] = quiz.id
                # Redirect to the main page with an activated "Play" button
                return redirect('index')

        # Difficulty is missing, handle error
        else:  
            print("Error: difficulty not found in POST request.")
            return redirect('index')  

    # Invalid request default redirect
    return redirect('index')

# Quiz Check Answer View
@login_required
def quiz_check_answer(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        user_answer = request.POST.get('user_answer').strip().lower()

        # Get the question object
        question = get_object_or_404(Question, id=question_id)
        correct_answer = question.correct_answer.strip().lower()

        # Store question, user's answer, and correct answer in the session
        request.session['question'] = question.translation_question
        request.session['user_answer'] = user_answer
        request.session['correct_answer'] = correct_answer

        # Increment correct/incorrect counts in session
        correct_count = request.session.get('correct_count', 0)
        incorrect_count = request.session.get('incorrect_count', 0)

        # Determine if the answer is correct or incorrect
        if user_answer == correct_answer:
            request.session['correct_count'] = correct_count + 1
            return redirect('quiz_correct')
        else:
            request.session['incorrect_count'] = incorrect_count + 1
            return redirect('quiz_incorrect')

    # Redirect to the quiz page if the request method is not POST
    return redirect('quiz')

# Quiz Correct View 
@login_required
def quiz_correct(request):
    # Retrieve data from the session
    question = request.session.get('question')
    user_answer = request.session.get('user_answer')

    # Pool of positive feedback remarks
    positive_feedback = [
        "Great job!",
        "Fantastic!",
        "Well done!",
        "You're nailing it!",
        "Impressive!",
        "You got it!",
        "Correct!",
        "You're on a roll!",
        "Keep up the great work!",
        "Awesome job!",
        "You're doing amazing!",
        "Nice work!",
    ]

    # Randomly select a positive feedback remark
    feedback = random.choice(positive_feedback)

    # Load feedback for correct answers
    context = {
        'question': question,
        'user_answer': user_answer,
        'feedback': feedback
    }

    return render(request, 'quiz/quiz_correct.html', context)

# Quiz Incorrect View 
@login_required
def quiz_incorrect(request):
    # Retrieve data from the session
    question = request.session.get('question')
    user_answer = request.session.get('user_answer')
    correct_answer = request.session.get('correct_answer')

    # Pool of negative feedback remarks
    negative_feedback = [
        "So close! You'll get it next time!",
        "Almost! Keep it up!",
        "Don't give up, you're learning!",
        "Nice try! Keep practicing!",
        "Keep going, you'll get it soon!"
    ]

    # Randomly select a negative feedback remark
    feedback = random.choice(negative_feedback)

    # Load feedback for incorrect answers
    context = {
        'question': question,
        'user_answer': user_answer,
        'correct_answer': correct_answer,
        'feedback': feedback,
    }

    return render(request, 'quiz/quiz_incorrect.html', context)

# Quiz Recap View
@login_required
def quiz_recap(request):
    # Fetch progress from the session
    correct_count = request.session.get('correct_count', 0)
    incorrect_count = request.session.get('incorrect_count', 0)
    total_questions = correct_count + incorrect_count

    # Prepare the context for the recap page
    context = {
        'correct_count': correct_count,
        'incorrect_count': incorrect_count,
        'total_questions': total_questions,
        'score_percentage': (correct_count / total_questions) * 100 if total_questions > 0 else 0
    }

    # Clear progress after showing the recap
    request.session['correct_count'] = 0
    request.session['incorrect_count'] = 0

    return render(request, 'quiz/quiz_recap.html', context)

# Next/Try again should send POST or SOME kind of request after question feedback to update and load next question
def next_question(request):
    # Get the current question ID from the POST request
    question_id = request.session.get('question_id')
    quiz_id = request.session.get('quiz_id')

    # Get the quiz object
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Get the list of question IDs from the quiz
    question_ids = list(quiz.questions.values_list('id', flat=True))

    # Find the index of the current question
    current_index = question_ids.index(int(question_id))

    # Check if there is a next question
    if current_index < len(question_ids) - 1:
        # Get the next question ID
        next_question_id = question_ids[current_index + 1]

        # Retrieve the next question object
        next_question = get_object_or_404(Question, id=next_question_id)

        # Update the session with the next question data
        request.session['question'] = next_question.translation_question
        request.session['question_id'] = next_question.id

        # Pass the question number to the context
        question_number = current_index + 2  # Since we are 0-based, we add 2 to get the next question number

        context = {
            'quiz': quiz,
            'question': next_question,
            'question_number': question_number  # Add question number to the context
        }

        # Redirect to the quiz question page to display the next question
        return render(request, 'quiz/quiz_question.html', context)

    # No more questions left, redirect to the recap page or finish quiz
    return redirect('quiz_recap')


# word of the day
def word_of_the_day(request):
    return render(request, 'word_of_the_day.html', context)