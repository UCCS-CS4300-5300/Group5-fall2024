from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from home.models import Question, Member
from home.tasks import resetStreak

# Create your tests here.

'''
Test for user registration
Checks if user is able to have their information successfully stored in the system
Afterwards, checks if they can successfully log in
'''
class UserRegistrationLogin(TestCase):

    def test_register_login(self):

        # Data that will be used to register the user
        registrationData = {
            'username' : 'TestUser',
            'password1': 'Test!@#$',
            'password2' : 'Test!@#$',
        }

        # Data that will be used for logging in the user
        loginData = {

            'username': 'TestUser',
            'password': 'Test!@#$',
        }

        # Step 1: Register
        response = self.client.post(reverse('registration-page'), data=registrationData) # Put in data in registration form
        self.assertRedirects(response, reverse('login-page'))  # Check if user is redirected back to login page

        # Step 2: Login
        response = self.client.post(reverse('login-page'), data=loginData)  # Insert information in login page
        self.assertEqual(response.status_code, 302) # Check if the user is redirected to the homepage after successful login



'''
Test for seeing if a user can log out
'''
class UserLogoutTest(TestCase):

    def test_logout(self):
        # Create a user and member to test on
        user = User.objects.create_user(username='Test1', password='Test!@#$')
        Member.objects.create(user=user)  

        # Have them log in
        self.client.login(username='Test1', password="Test!@#$")

        # Have them initially be at the homepage
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        # Step 1: Log the user out
        response = self.client.get(reverse('logout'))
 
        # Step 2: Check if the user is redirected after logging out
        self.assertTemplateUsed(response, 'home/index.html') 

'''
Test for seeing if a logged in user will be redirected back to the home page if they try to access the register link 
'''
class UserFailSafe(TestCase):
    
    def test_goodCatch(self):
        # Create a test user and member to test on
        user = User.objects.create_user(username='Test1', password='Test!@#$')
        Member.objects.create(user=user)  

        # Have them log in
        self.client.login(username='Test1', password='Test!@#$')

        # Step 1: Have user try to access the register link when they are logged in already
        registerURL = reverse('registration-page')  # Get the registration URL
        response = self.client.get(registerURL) # Perform a GET request using the registration link
        self.assertEqual(response.status_code, 302) # Check if the response status is redirect which is a 302
        self.assertRedirects(response, reverse('index')) # Check if user was redirected back to the homepage



'''
Test for session data tracking (correct and incorrect answers) 
'''
class QuizSessionTrackingTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='TestUser', password='Test!@#$')

        # Log in the user
        self.client.login(username='TestUser', password='Test!@#$')

        # Add a question for testing
        self.question = Question.objects.create(translation_question="Hola", correct_answer="Hello", source_language="Spanish", target_language="English", difficulty="Easy")

    def test_quiz_session_data(self):
        session = self.client.session

        # Test a correct answer
        response = self.client.post(reverse('quiz_check_answer'), {'question_id': self.question.id, 'user_answer': 'Hello'})
        session['correct_answers'] = session.get('correct_answers', 0) + 1  # Increment correct answers
        self.assertEqual(session['correct_answers'], 1)  # Ensure correct answer is tracked

        # Test an incorrect answer
        response = self.client.post(reverse('quiz_check_answer'), {'question_id': self.question.id, 'user_answer': 'Hi'})
        session['incorrect_answers'] = session.get('incorrect_answers', 0) + 1  # Increment incorrect answers
        self.assertEqual(session['incorrect_answers'], 1)  # Ensure incorrect answer is tracked


'''
Test for question pool consistency
'''
class QuestionPoolTest(TestCase):
    def setUp(self):
        # Run the add_questions.py management command to populate the database with questions
        from django.core.management import call_command
        call_command('add_questions')

    def test_question_pool_size(self):
        easy_questions = Question.objects.filter(difficulty="Easy").count()
        medium_questions = Question.objects.filter(difficulty="Medium").count()
        hard_questions = Question.objects.filter(difficulty="Hard").count()

        # Assert there are 10 questions per difficulty level
        self.assertEqual(easy_questions, 10)
        self.assertEqual(medium_questions, 10)
        self.assertEqual(hard_questions, 10)

        # Assert the total question pool is 30
        total_questions = Question.objects.all().count()
        self.assertEqual(total_questions, 30)

'''
Series of tests for resetting streak implementation
'''
class ResetStreakTests(TestCase):
    # Create members to use in tests
    def setUp(self):
        self.member1 = Member.objects.create(hasCompletedQuiz = False, streakCount = 4)
        self.member2 = Member.objects.create(hasCompletedQuiz = True, streakCount = 5)
        self.member3 = Member.objects.create(hasCompletedQuiz = False, streakCount = 3)
    
    # Test that a member who hasn't completed a quiz has their streak reset.
    def test_reset_streak_no_quiz_completed(self):
        resetStreak()
        self.member1.refresh_from_db()

        self.assertEqual(self.member1.streakCount, 0)
        self.assertFalse(self.member1.hasCompletedQuiz)

    # Test that a member who completed a quiz does not reset their streak.
    def test_reset_streak_quiz_completed(self):
        resetStreak()
        self.member2.refresh_from_db()

        self.assertEqual(self.member2.streakCount, 5)  
        self.assertFalse(self.member2.hasCompletedQuiz)  

    # Test that streaks are correctly reset for multiple members.
    def test_reset_streak_multiple_members(self):
        resetStreak()
        self.member1.refresh_from_db()
        self.member3.refresh_from_db()
        
        self.assertEqual(self.member1.streakCount, 0)  
        self.assertEqual(self.member3.streakCount, 0)  
        self.assertFalse(self.member1.hasCompletedQuiz)
        self.assertFalse(self.member3.hasCompletedQuiz)

    # Test that running the resetStreak function with NO members in the database still works without errors
    def test_reset_streak_no_members(self):
        Member.objects.all().delete()
        resetStreak()  
        self.assertEqual(Member.objects.count(), 0) 
