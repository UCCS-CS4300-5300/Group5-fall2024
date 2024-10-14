from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

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

        # Create a user to test on
        self.user = User.objects.create_user(username='Test1', password='Test!@#$')

        # Have this user be logged in
        self.client.login(username='Test1', password="Test!@#$")

        # Have them initially be at the homepage
        response = self.client.get(reverse('index'))

        # Check if the user is logged in 
        self.assertEqual(response.status_code, 200)

        # Step 1: Log the user out
        response = self.client.get(reverse('logout'))
        
        #Step 2: Check if the user is on homepage after logging out
        self.assertTemplateUsed(response, 'home/index.html')


'''
Test for seeing if a logged in user will be redirected back to the home page if they try to access the register link 
'''
class UserFailSafe(TestCase):
    def test_goodCatch(self):

        # Create a test user
        self.user = User.objects.create_user(username='Test1', password='Test!@#$')

        # Have them log in
        self.client.login(username='Test1', password='Test!@#$')

        # Have them initially at homepage
        response = self.client.get(reverse('index'))

        # Step 1: Have user try to access the register link when they are logged in already
        registerURL = reverse('registration-page')  # Get the registration URL
        response = self.client.get(registerURL) # Perform a GET request using the registration link
        self.assertEqual(response.status_code, 302) # Check if the response status is redirect which is a 302
        self.assertRedirects(response, reverse('index')) # Check if user was redirected back to the homepage