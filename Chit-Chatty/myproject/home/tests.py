from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from home.models import Quiz, Question, Member
from home.tasks import resetStreak
from unittest.mock import patch
import json


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
class QuizTests(TestCase):
    def setUp(self):
        # Create a test user and member
        self.user = User.objects.create_user(username='TestUser', password='TestPass123')
        self.member = Member.objects.create(
            user=self.user,
            userName='TestUser',
            streakCount=0,
            hasCompletedQuiz=False
        )
        self.client = Client()
        self.client.login(username='TestUser', password='TestPass123')

    def test_quiz_generation(self):
        # Set up data to send for quiz generation
        generate_url = reverse('generate_quiz')
        data = {'difficulty': 'easy'}  # Example difficulty level
        
        # Send POST request to generate quiz
        response = self.client.post(generate_url, data)

        # Retrieve the created quiz
        quiz = Quiz.objects.filter(is_next=True).first()

        # Assertions
        self.assertEqual(response.status_code, 302)  # Should redirect after creation
        self.assertIsNotNone(quiz, "Quiz should be created and marked as next quiz.")
        self.assertGreater(quiz.questions.count(), 0, "Quiz should have questions associated.")

    def test_quiz_completion(self):
        # Set up a quiz for the user
        quiz = Quiz.objects.create(title="Test Quiz", description="A test quiz", is_next=True)
    
        # Create and link questions to the quiz
        questions = [
            Question.objects.create(
                translation_question=f"Question {i}",
                correct_answer=f"Answer {i}",
                source_language="Spanish",
                target_language="English"
            ) for i in range(1, 6)
        ]
        quiz.questions.add(*questions)
    
        # Start quiz and simulate answering questions
        for question in questions:
            check_answer_url = reverse('quiz_check_answer')
            self.client.post(check_answer_url, {'question_id': question.id, 'user_answer': question.correct_answer})

        # Move to the recap view to mark the quiz as complete
        recap_url = reverse('quiz_recap')
        self.client.get(recap_url)

        # Refresh data to reflect post-recap view updates
        quiz.refresh_from_db()
        self.member.refresh_from_db()

        # Assertions to verify the quiz completion status
        self.assertTrue(self.member.hasCompletedQuiz, "Member should be marked as having completed the quiz.")
        self.assertEqual(self.member.streakCount, 1, "Member's streak count should increment by 1.")

'''
Tests for resetting streak implementation
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

'''
Test for answering the word of the day
'''
class WordOfTheDayTests(TestCase):
    # Set up the test client and define the URL for the word of the day view
    def setUp(self):
        self.client = Client()
        self.url = reverse('word_of_the_day')

    @patch('requests.get')
    def test_word_of_the_day_success(self, mock_get):
        # Mocking the API response for a successfull call
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'word': '你好', 'definition': 'Hello'}]

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '你好') 
        self.assertEqual(self.client.session['word_of_the_day'], '你好')
        self.assertEqual(self.client.session['english_translation'], 'Hello')

    def test_word_of_the_day_incorrect(self):
        # Simulate setting the word and translation in session
        self.client.session['word_of_the_day'] = '你好'
        self.client.session['english_translation'] = 'Hello'

        response = self.client.post(self.url, {'user_guess': 'Hi'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Uh oh, better luck next time')
        self.assertNotIn('word_of_the_day', self.client.session)

'''
Test for selecting a language
'''
class SetLanguageTests(TestCase):
    # Set up the test client and define the URL for the set language view
    def setUp(self):
        self.client = Client()
        self.url = reverse('set_language')

    def test_set_language_success(self):
        # Simulate a successful language change with a POST request
        response = self.client.post(self.url, json.dumps({'language': 'chinese'}), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True})
        self.assertEqual(self.client.session['selected_language'], 'chinese')
