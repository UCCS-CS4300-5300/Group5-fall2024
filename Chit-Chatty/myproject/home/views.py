from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import Quiz, Member, Question
from .forms import CreateUserForm
from .decorators import unauthenticatedUser
from django.utils.safestring import mark_safe
from .services import generate_translation_questions, get_word_of_the_day
import random
import requests
import json
import datetime

# Home Page View
def index(request):
    if request.method == "POST":
        selected_difficulty = request.POST.get("difficulty")
        selected_length = request.POST.get("num_questions")
        selected_goal = request.POST.get("learning_goal")

        # Update session with submitted values
        if selected_difficulty:
            request.session["selected_difficulty"] = selected_difficulty
        if selected_length:
            request.session["selected_length"] = selected_length
        if selected_goal:
            request.session["selected_goal"] = selected_goal

    # Check if there is an active quiz in the session
    active_quiz = None
    if "quiz_id" in request.session:
        try:
            active_quiz = Quiz.objects.get(id=request.session["quiz_id"], is_completed=False)
        except Quiz.DoesNotExist:
            active_quiz = None  # If no active quiz is found

    context = {
        "selected_language": request.session.get("selected_language", "chinese"),
        "selected_difficulty": request.session.get("selected_difficulty", "Easy"),
        "selected_length": request.session.get("selected_length", 5),
        "selected_goal": request.session.get("selected_goal", "Travel"),
        "active_quiz": active_quiz,  # Include the active quiz if it exists
    }

    return render(request, "home/index.html", context)


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
View for the account details page of a user
'''
@login_required(login_url='login-page')
def accountPage(request, userID):
    
    # Ensures that only the user can view their own account details page and not view others
    # Returns user back to homepage
    if (request.user.id != userID):
          return redirect('index')

    # Otherwise, grab the Member object associated with the user
    member = get_object_or_404(Member, user=request.user)

    # Go to the account page 
    return render(request, 'authentication/account_details.html', {'member': member})

'''
View for updating account details
The reason it's so long is because the 'User' object in the 'Member' object also has a username, first_name, last_name, and email field so it has to be update there too.
'''
@login_required(login_url='login-page')
def update_account_details(request):
    if request.method == 'POST':
        # Grab the member from the database
        member = Member.objects.filter(user = request.user).first()
        
        # Get data from the POST request
        username = request.POST.get('usernameEditField')
        email = request.POST.get('emailEditField')
        firstName = request.POST.get('firstNameEditField')
        lastName = request.POST.get('lastNameEditField')

        # Update the username field
        if username and username != member.userName:
            # Checks if username already exists in the database. If it does, return an error.
            if Member.objects.filter(userName=username).exists():
                messages.error(request, "Username already taken. Please choose another.")
                return redirect('account_details', request.user.id)

            # Update the username in the database
            member.userName = username
            member.user.username = username  
            messages.success(request, "Updated username")

        # Update the email field
        if email and email != member.email: 
            member.email = email
            member.user.email = email 
            messages.success(request, "Updated email")

        # Update the first name field
        if firstName and firstName != member.firstName:
            member.firstName = firstName
            member.user.first_Name = firstName 
            messages.success(request, "Updated first name")
        
        # Update the last name field
        if lastName and lastName != member.lastName:
            member.lastName = lastName
            member.user.last_Name = lastName  
            messages.success(request, "Updated last name")

        # Save both the User and Member updates
        member.save() 
        member.user.save()  

        # Redirect to the account page
        return redirect('account_details', request.user.id )

    # If the request method is not POST, redirect to homepage
    return redirect('index')

def update_account(request):
    if request.method == 'POST':
        user = request.user.member
        username = request.POST.get('username')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')

'''
View for logging out
Redirects user back to the login-page no matter what (because returning render after logging out isn't executing for some reason)
'''
@login_required(login_url='login-page')
def logout(request):
    auth_logout(request) 
    return render(request, 'home/index.html')

# Quiz Views
@login_required
def quiz(request):
    # Reset the session when starting a new quiz
    request.session['correct_count'] = 0
    request.session['incorrect_count'] = 0
    request.session['question_id'] = 1

    # Fetch the next quiz and the first question
    next_quiz = Quiz.objects.filter(is_next=True, is_completed=False).first()
    print("Fetched quiz:", next_quiz)

    if next_quiz:
        first_question = next_quiz.questions.first()
        print("First question in quiz:", first_question)

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


@login_required
def generate_quiz(request):
    # Check for POST request with selected parameters
    if request.method == 'POST':
        print(f"Received POST request with data: {request.POST}")
        
        # Retrieve quiz parameters from POST data
        proficiency = request.POST.get('proficiency')
        difficulty = request.POST.get('difficulty')
        num_questions = request.POST.get('num_questions')
        goal = request.POST.get('learning_goal')

        if difficulty and num_questions and goal:
            # Retrieve selected languages from session
            source_lang = request.session.get('selected_language', 'Arabic')  # default to 'Chinese'
            target_lang = 'English'

            # Generate structured output with title, description, and questions
            structured_output = generate_translation_questions(proficiency, difficulty, source_lang, target_lang, int(num_questions), goal)
            print("Generated structured output:", structured_output)  # Debug statement

            # Create a new quiz with title and description
            quiz = Quiz.objects.create(
                title=structured_output.get('title', 'Default Title'),
                description=structured_output.get('description', 'Default Description'),
                is_next=True
            )

            # Loop through questions and save each to the database
            for item in structured_output.get('questions', []):
                question_text = item['question']
                translated_answer = item['translation']
                print("Saving question:", question_text)  # Debug statement

                # Save question to the database
                question = Question.objects.create(
                    translation_question=question_text,
                    correct_answer=translated_answer,
                    source_language=source_lang,
                    target_language=target_lang,
                )
                quiz.questions.add(question)  # Link question to quiz

            # Mark the quiz as "Next" and save it
            quiz.is_next = True
            quiz.save()

            # Save quiz details to session and redirect
            request.session['quiz_id'] = quiz.id
            request.session['quiz_title'] = structured_output.get('title', 'Default Title')
            request.session['quiz_description'] = structured_output.get('description', 'Default Description')
            request.session['difficulty'] = difficulty
            request.session['length'] = num_questions
            
            return redirect('quiz_start')  
        else:
            print("Error: missing one or more parameters in POST request.")
            return redirect('index')  

    return redirect('index')


# Quiz Start View
@login_required
def quiz_start(request):
    # Retrieve quiz details from session
    quiz_title = request.session.get('quiz_title', 'Quiz Title')
    quiz_description = request.session.get('quiz_description', 'Quiz Description')
    difficulty = request.session.get('difficulty', 'Easy')
    length = request.session.get('length', 5)

    context = {
        'quiz_title': quiz_title,
        'quiz_description': quiz_description,
        'difficulty': difficulty,
        'length': length,
    }
    return render(request, 'quiz/quiz_start.html', context)


# Views to prompt the user with quiz options
@login_required
def continue_quiz(request):
    quiz_id = request.session.get("quiz_id")
    quiz_title = request.session.get('quiz_title', 'Quiz Title')
    quiz_description = request.session.get('quiz_description', 'Quiz Description')
    difficulty = request.session.get('difficulty', 'Easy')
    length = request.session.get('length', 5)
    
    if not quiz_id:
        return redirect('index')

    # Retrieve the active quiz and ensure it's incomplete
    quiz = get_object_or_404(Quiz, id=quiz_id, is_completed=False)

    quiz.questions.clear()

    # Ensure length is an integer
    try:
        selected_length = int(length)
    except ValueError:
        selected_length = 5

    # Band-Aid Solution
    # Fetch new questions
    new_questions = Question.objects.all()[:selected_length]
    quiz.questions.set(new_questions)

    quiz.is_active = True
    quiz.save()

    context = {
        'quiz_title': quiz_title,
        'quiz_description': quiz_description,
        'difficulty': difficulty,
        'length': length,
    }
    return render(request, 'quiz/quiz_start.html', context)


@login_required
def exit_quiz(request):
    quiz_id = request.session.get("quiz_id")
    if quiz_id:
        quiz = get_object_or_404(Quiz, id=quiz_id)
        user = quiz.user

        # Mark quiz as incomplete instead of inactive
        quiz.is_completed = False
        quiz.save()
        return redirect('index')  # Redirect to the index page

    return JsonResponse({"error": "No active quiz to exit"}, status=400)


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
    score_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0

    # Retrieve the quiz from the session and mark it as completed
    quiz_id = request.session.get('quiz_id')
    if quiz_id:
        quiz = get_object_or_404(Quiz, id=quiz_id)
        quiz.is_completed = True
        quiz.is_next = False  # Always mark as not the next quiz
        quiz.score = score_percentage
        quiz.save()

        # Check if the action is 'try_again' or 'finish'
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'try_again':
                # Reset the quiz for retry
                quiz.is_next = True
                quiz.is_completed = False
                quiz.save()
                
                # Reset session progress
                request.session['correct_count'] = 0
                request.session['incorrect_count'] = 0
                request.session['quiz_id'] = quiz.id
                
                return redirect('quiz')
            elif action == 'finish':
                # Clear quiz session ID and progress as quiz is complete
                request.session.pop('quiz_id', None)
                request.session['correct_count'] = 0
                request.session['incorrect_count'] = 0
                Quiz.objects.filter(user=request.user.member).delete()
                Question.objects.filter(quiz__user=request.user.member).delete()

                quiz.delete()
                return redirect('index')

    # Prepare the context for the recap page
    context = {
        'correct_count': correct_count,
        'incorrect_count': incorrect_count,
        'total_questions': total_questions,
        'score_percentage': score_percentage,
    }

    # Update user's quiz completion status
    # Also updates their longest streak variable
    member = request.user.member
    if not member.hasCompletedQuiz:
        member.hasCompletedQuiz = True
        member.streakCount += 1
        if (member.streakCount > member.longestStreak):
            member.longestStreak = member.streakCount
        member.save()

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


# word of the day using openai
def word_of_the_day(request):
    selected_language = request.session.get('selected_language', 'arabic').lower()

    # Fetch word and translation if necessary
    if 'word_of_the_day' not in request.session or request.session.get('language_for_word') != selected_language:
        word_data = get_word_of_the_day(selected_language)
        word_of_the_day = word_data.get('word_of_the_day')
        english_translation = word_data.get('english_translation')
        print("Returned from get_word_of_the_day:", word_of_the_day, english_translation)

        if word_of_the_day:
            request.session['word_of_the_day'] = word_of_the_day
            request.session['english_translation'] = english_translation
            request.session['language_for_word'] = selected_language
            print("Fetched word of the day:", word_of_the_day)
        else:
            return render(request, 'home/word_of_the_day.html', {
                'error': "Could not find a word of the day."
            })

    # Retrieve values from session
    word_of_the_day = request.session.get('word_of_the_day')
    print("Word of the Day in session:", word_of_the_day)
    english_translation = request.session.get('english_translation')
    result = None

    # Handle user guess
    if request.method == 'POST':
        user_guess = request.POST.get('user_guess')
        if user_guess.lower() == english_translation.lower():
            result = mark_safe('Correct! <br>&emsp;<strong>ᕦ(ò_óˇ)ᕤ</strong>')
        else:
            result = mark_safe(f'Uh oh, the correct answer is: <strong>{english_translation}</strong> <br>Try again tomorrow <br>&emsp;<strong>ʅ（◞‿◟）ʃ</strong>')

        # Clear session for a new word on the next visit
        for key in ['word_of_the_day', 'english_translation']:
            request.session.pop(key, None)

    return render(request, 'home/word_of_the_day.html', {
        'word_of_the_day': word_of_the_day,
        'selected_language': selected_language.capitalize(),
        'result': result,
    })


@csrf_exempt
def set_language(request):
    
    if request.method == "POST":
        data = json.loads(request.body)
        language = data.get('language')
        
        # Save to session
        request.session['selected_language'] = language
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False}, status=400)


# daily lesson
def daily_lesson(request):
    # set a default language if not already set
    selected_language = request.session.get('selected_language', 'arabic').lower()
    print(f"View selected_language: {selected_language}")

    context = {
    'selected_language': selected_language
    }

    # gives the current day of year (each day 1-7)
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    # cycle through lessons
    total_lessons = 7
    lesson_number = (day_of_year % total_lessons) + 1

    # dynamically select the corresponding lesson template
    template_name = f"daily_lesson/lesson{lesson_number}.html"

    # to test individual templates
    # template_name = f"daily_lesson/lesson1.html"
    
    return render(request, template_name, context)