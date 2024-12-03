from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from home.models import Quiz, Question, Member
from home.tasks import resetStreak
from unittest.mock import patch
import json


# Test for user registration
# Checks if user is able to have their information successfully
# stored in the system. Afterwards, checks if they can successfully log in
class UserRegistrationLogin(TestCase):

    def test_register_login(self):

        # Data that will be used to register the user
        registrationData = {
            'username': 'TestUser',
            'password1': 'Test!@#$',
            'password2': 'Test!@#$',
        }

        # Data that will be used for logging in the user
        loginData = {

            'username': 'TestUser',
            'password': 'Test!@#$',
        }

        # Step 1: Register
        # Put in data in registration form
        response = self.client.post(reverse('registration-page'), data=registrationData)  # noqa: E501
        # Check if user is redirected back to login page
        self.assertRedirects(response, reverse('login-page'))

        # Step 2: Login
        # Insert information in login page
        response = self.client.post(reverse('login-page'), data=loginData)
        # Ensure user is redirected to the homepage after successful login
        self.assertEqual(response.status_code, 302)


# Test for seeing if a user can log out
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

        # Step 2: Ensure user is redirected after logging out
        self.assertTemplateUsed(response, 'home/index.html')


# Test for seeing if a logged in user will be redirected back
# to the home page if they try to access the register link

class UserFailSafe(TestCase):

    def test_goodCatch(self):
        # Create a test user and member to test on
        user = User.objects.create_user(username='Test1', password='Test!@#$')
        Member.objects.create(user=user)

        # Have them log in
        self.client.login(username='Test1', password='Test!@#$')

        # Step 1:
        # Have user try to access the register link when they are logged in already  # noqa: E501
        # Get the registration URL
        registerURL = reverse('registration-page')
        # Perform a GET request using the registration link
        response = self.client.get(registerURL)
        # Ensure response status is redirect which is a 302
        self.assertEqual(response.status_code, 302)
        # Check if user was redirected back to the homepage
        self.assertRedirects(response, reverse('index'))


# Test for seeing if a logged in user can update their account settings
class AccountDetailsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')  # noqa: E501
        self.member = Member.objects.create(
            user=self.user,
            userName='testuser',
            email='testuser@example.com',
            firstName='Test',
            lastName='User',
            streakCount=5,
            longestStreak=10
        )

        self.client.login(username='testuser', password='password123')

    def test_account_page_load(self):
        """Test that the account details page loads correctly"""
        response = self.client.get(reverse('account_details', args=[self.user.id]))  # noqa: E501
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account Details')
        self.assertContains(response, self.member.userName)
        self.assertContains(response, self.member.email)

    def test_update_account_details(self):
        """Test updating only some fields (e.g., email only)"""
        # Update only email
        response = self.client.post(reverse('update_account_details'), {
            'emailEditField': 'partialupdate@example.com',
        })

        # Assert that the user is redirected to the account details page
        self.assertRedirects(response, reverse('account_details', args=[self.user.id]))  # noqa: E501

        # Retrieve the updated member object from the database
        updated_member = Member.objects.get(user=self.user)

        # Assert that the email has been updated
        self.assertEqual(updated_member.email, 'partialupdate@example.com')


# Test for session data tracking (correct and incorrect answers)
class QuizTests(TestCase):
    def setUp(self):
        # Create a test user and member
        self.user = User.objects.create_user(username='TestUser', password='TestPass123')  # noqa: E501
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
        data = {
            'difficulty': 'Easy',
            'num_questions': 5,
            'learning_goal': 'Travel'
        }

        # Send POST request to generate quiz
        response = self.client.post(generate_url, data)

        # Retrieve the created quiz
        quiz = Quiz.objects.filter(is_next=True).first()

        # Assertions
        self.assertEqual(response.status_code, 302)  # Should redirect after creation  # noqa: E501
        self.assertIsNotNone(quiz, "Quiz should be created and marked as next quiz.")  # noqa: E501
        self.assertGreater(quiz.questions.count(), 0, "Quiz should have questions associated.")  # noqa: E501

    def test_quiz_completion(self):
        # Set up a quiz for the user
        quiz = Quiz.objects.create(title="Test Quiz", description="A test quiz", is_next=True)  # noqa: E501

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
            self.client.post(check_answer_url, {'question_id': question.id, 'user_answer': question.correct_answer})  # noqa: E501

        # Move to the recap view to mark the quiz as complete
        recap_url = reverse('quiz_recap')
        self.client.get(recap_url)

        # Refresh data to reflect post-recap view updates
        quiz.refresh_from_db()
        self.member.refresh_from_db()

        # Assertions to verify the quiz completion status
        self.assertTrue(self.member.hasCompletedQuiz, "Member should be marked as having completed the quiz.")  # noqa: E501
        self.assertEqual(self.member.streakCount, 1, "Member's streak count should increment by 1.")  # noqa: E501


# Tests for quiz continuation implementation
class QuizExitAndContinueTests(TestCase):
    def setUp(self):
        # Create a test user and log them in
        self.user = User.objects.create_user(username='TestUser', password='TestPass123')  # noqa: E501
        self.client = Client()
        self.client.login(username='TestUser', password='TestPass123')  # noqa: E501

        # Create a quiz and assign it as an active session quiz
        self.quiz = Quiz.objects.create(title="Test Quiz", description="A test quiz", is_completed=False)  # noqa: E501
        self.question = Question.objects.create(
            translation_question="Translate 'casa'",
            correct_answer="house",
            source_language="Spanish",
            target_language="English"
        )
        self.quiz.questions.add(self.question)
        self.quiz.save()

        # Set session data for an active quiz
        session = self.client.session
        session['quiz_id'] = self.quiz.id
        session['quiz_title'] = self.quiz.title
        session['quiz_description'] = self.quiz.description
        session['difficulty'] = 'Easy'
        session['length'] = 1
        session.save()

    def test_exit_quiz(self):
        # Step 1: Exit the quiz
        exit_url = reverse('exit_quiz')
        response = self.client.get(exit_url)

        self.quiz.refresh_from_db()
        self.assertRedirects(response, reverse('index'), msg_prefix="Exiting quiz should redirect to index.")  # noqa: E501
        self.assertFalse(self.quiz.is_completed, "Quiz should remain incomplete after exit.")  # noqa: E501

        # Step 2: Return to the index page and check for "Continue Quiz" option
        index_url = reverse('index')
        response = self.client.get(index_url)

        self.assertContains(response, "Continue Quiz", msg_prefix="Index page should show 'Continue Quiz' option.")  # noqa: E501


# Tests for resetting streak implementation
class ResetStreakTests(TestCase):
    # Create members to use in tests
    def setUp(self):
        self.member1 = Member.objects.create(hasCompletedQuiz=False, streakCount=4)  # noqa: E501
        self.member2 = Member.objects.create(hasCompletedQuiz=True, streakCount=5)  # noqa: E501
        self.member3 = Member.objects.create(hasCompletedQuiz=False, streakCount=3)  # noqa: E501

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

    # Test that running the resetStreak function with NO members
    # in the database still works without errors
    def test_reset_streak_no_members(self):
        Member.objects.all().delete()
        resetStreak()
        self.assertEqual(Member.objects.count(), 0)


# Test for answering the word of the day
class WordOfTheDayTest(TestCase):

    def setUp(self):
        """
        Setup initial data for Word of the Day feature testing.
        Create a user and member.
        """
        user = User.objects.create_user(username='testuser', password='12345')  # noqa: E501
        self.member = Member.objects.create(user=user, userName='testuser')  # noqa: E501
        # Log the user in
        self.client.login(username='testuser', password='12345')

    def test_word_of_the_day_view(self):
        """
        Test the word of the day functionality by checking if the page renders correctly,  # noqa: E501
        and the word and translation are stored in the session.
        """
        # Access the Word of the Day view
        response = self.client.get(reverse('word_of_the_day'))

        # Ensure page loads correctly
        self.assertEqual(response.status_code, 200)

        # Ensure word and translation are set in the session
        self.assertIn('word_of_the_day', self.client.session)
        self.assertIn('english_translation', self.client.session)

        # Ensure page contains the word of the day
        word_of_the_day = self.client.session.get('word_of_the_day')
        self.assertContains(response, word_of_the_day)

    def test_user_guess_correct(self):
        """
        Test that the user can correctly guess the word of the day and get a 'Correct' response.  # noqa: E501
        """
        # First, make sure we have a word of the day in the session
        self.client.get(reverse('word_of_the_day'))

        # Define the correct translation
        correct_translation = self.client.session.get('english_translation')

        # Send a POST request with the correct guess
        response = self.client.post(reverse('word_of_the_day'), {'user_guess': correct_translation})  # noqa: E501

        # Check that the result is 'Correct!'
        self.assertContains(response, 'Correct!')

        # Ensure word and translation are cleared from the session for the next visit  # noqa: E501
        self.assertNotIn('word_of_the_day', self.client.session)
        self.assertNotIn('english_translation', self.client.session)


# Test for selecting a language
class SetLanguageTests(TestCase):
    # Set up the test client and define the URL for the set language view
    def setUp(self):
        self.client = Client()
        self.url = reverse('set_language')

    def test_set_language_success(self):
        # Simulate a successful language change with a POST request
        response = self.client.post(self.url,
                                    json.dumps({'language': 'chinese'}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True})
        self.assertEqual(self.client.session['selected_language'], 'chinese')
