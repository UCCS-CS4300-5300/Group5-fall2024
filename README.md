# ChitChatty Language Learning Application

#### Created by Darion Badillo, Andrew Douangprachanh, Irving Reyes Bravo, Naomi Rodriguez, and Christopher Romo
#### CS 4300 Advanced Software Engineering : Group 5 : Fall 2024

---
## App Overview

**ChitChatty** is a language learning platform designed to help users improve their language skills through custom quizzes and pre-made lessons. The app integrates AI tools and user input to generate custom quizzes. Word of the day and the daily lesson encourages continuous learning. Multiple languages are supported. The app aims to provide an engaging and personalized learning experience by adapting the learning material to your preferences.

---
## App Features

### 1. User Authentication
   - User registration, login, and session management.
   - Users have their own account page with saved data like streaks.

### 2. Dynamic AI Quiz Generation
   - Translation questions are created based on the options the user selects.
   - User can select their preferred Language, Proficiency, Difficulty, Length of Quiz, and Goal of Quiz.

### 3. Quiz Management
   - User progress is tracked during quizzes.
   - Session data is maintained for correct and incorrect answers.
   - Quiz can be stopped and restarted.

### 5. Quiz Recap
   - Display the user’s score at the end of each quiz.
   - Recap page provides a summary of the quiz, including correct and incorrect answers and overall performance.

### 6. Word of the Day
   - Single word daily quiz based on selected language.
   - Immediate feedback provided based on answer.

### 7. Daily Lesson
   - Lesson based on a theme to encourage learning.
   - 8 cards with images appear with translations, allowing for visual learning.
   - Lessons change out daily.

### 8. Friendly UI
   - Clean and user-friendly interface with Bootstrap-based styling.
   - Responsive pages to adapt to user's browser.
   - Styled to foster a fun learning atmosphere.

---
## App Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ChitChatty.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the server:

   ```bash
   python manage.py runserver
   ```

6. Access the app at `http://127.0.0.1:8000`.

---
## App Testing

### How to Test
1. Install this Django environment's required packages:
	```bash
   pip install -r requirements.txt
   ```
2. Apply all database migrations before running tests:
	```bash
 	python manage.py migrate
 	```
3. Run the test suite to execute the defined tests:
	```bash
 	python manage.py test
 	```

### List of Tests
1. **User Registration and Login**: Tests user registration and login process.
	- Steps:
	- Registers a user with provided credentials.
	- Logs the user in and verifies successful redirection to the homepage.
2. **User Logout**: Tests the logout functionality.
	- Steps:
	- Logs in a user, then verifies they are logged out and redirected to the homepage.
3. **User Fail-Safe**: Ensures a logged-in user is redirected to the homepage if they try to access the registration page.
	- Steps:
	- Logs in a user and tries to access the registration page.
	- Verifies they are redirected back to the homepage.
4. **Account Details Update**: Tests updating account details (e.g., email).
	- Steps:
	- Loads the account details page.
	- Updates the email field and verifies the changes are saved and reflected on the account page.
5. **Quiz Generation and Completion**: Tests the generation and completion of quizzes.
	- Steps:
	- Generates a quiz with specific parameters (difficulty, number of questions).
	- Verifies the quiz is created and contains questions.
	- Completes the quiz and checks if streaks are updated and the quiz is marked as completed.
6. **Quiz Exit and Continuation**: Tests the quiz exit and continuation functionality.
	- Steps:
 	- Exits an ongoing quiz and verifies the quiz status.
	- Verifies that the option to continue the quiz is available on the homepage.
7. **Streak Reset**: Tests resetting streaks for users who have or have not completed a quiz.
	- Steps:
	- Resets streaks for users who haven’t completed a quiz.
	- Verifies that streaks are reset and that users who have completed quizzes retain their streaks.
8. **Word of the Day**: Tests the functionality of the Word of the Day feature.
	- Steps:
	- Verifies the correct display of the Word of the Day and its translation.
	- Tests the user's ability to correctly guess the word and receive feedback.
	Verifies the session is cleared after a correct guess.
9. **Set Language**: Tests that the user an succesfully change the selected language in the session.
	- Steps:
	- Defines the url for the set language view after setting up a test client.
	- Simulates a successful language change with a POST request.  
10. **Daily Lesson**: Tests the functionality of the Daily Lesson feature.
	- Steps:
	- Verifies the mocked day of the year (should be 345 for Dec 10).
	- Make the request without setting a session language (default to Arabic).
	- Verifies the expected lesson based on the mocked day of the year.

### How to view Test Coverage
1. Verify that the Coverage package is installed:
	```bash
	pip install coverage
 	```
2. Run your tests while measuring code coverage:
	```bash
 	coverage python manage.py test
 	```
3. After the tests finish, generate a coverage report:
	```bash
 	coverage report -m
 	```
 4. Alternatively, you can view the latest (12/10/24) coverage report text:
	```bash
 	cat coverage_report.txt
 	```

---
## App Changelog

Listed below are all changes made to the app based on sprint.

---
## Sprint 1 (10/17/2024)

### Quiz Logic - Darion Badillo

**ADDED**
   - The Question model with the following fields:
      - Foreign key to Quiz
      - translation_question to hold the source language phrase
      - correct_answer to store the correct translation
      - source_language and target_language fields
      - difficulty to categorize questions into Easy, Medium, or Hard
   - A M:N relationship between quizzes and generated questions
   - Management/Commands directory to manage dynamic question loading
   - Implemented a command that adds 30 translation questions (10 for each difficulty) into the database
   - Implemented the next_question view to handle question progression
   - A quiz_recap template and view that provides a recap of quiz performance
   - Handled session variables for quiz progress (correct_count, incorrect_count, question_id) to ensure smooth tracking of user performance
   - Pools of positive and negative feedback in the quiz_correct and quiz_incorrect views to display random feedback after each question

**UPDATED**
   - Adjusted the Quiz model to include a boolean is_next flag to indicate the next quiz
   - Moved all quiz templates into a newly created quiz folder under templates
   - Filled out views for quiz operations including quiz, quiz_recap, quiz_correct, quiz_incorrect, and next_question 
   - Adjusted the generate_quiz view to handle dynamic quiz generation based on difficulty
   - Fixed how question IDs are linked to quizzes to prevent the same question from being displayed repeatedly
   - Ensured the Play button has a consistent 3D appearance with enhanced depth and shadows for better visual feedback
   - The dropdown menus in the navbar no longer hover or float unintentionally
   - Dropdown selections are now properly displayed, reflecting the chosen difficulty level
   - Separated the Play button styling from other items in the `styles.css` file
   - Fixed the hover behavior of the Play button to lift up instead of enlarging
   - Made the Play button dynamically scale when active and ensured it remains aligned with the card element
   - Disabled the Play button if no quiz is available

### Account Features - Andrew Douangprachanh

**ADDED**
   - the ability for the user to create an account and log in to the website
   - two new templates in the "authentication" folder called `login.html` and `register.html`
   - `forms.py`, which allows for defining a form with information that must be filled by the user to register
   - `decorators.py`. So far, it only has one decorator that prevents logged-in users from accessing the registration and login links
   - pytests to ensure that logging in, logging out, and failsafes work correctly

**UPDATED**
   - `models.py` to include a new model called "Member," which represents a single user and contains fields such as first and last name
   - `urls.py` to include links for registration, logging in, and logging out
   - `views.py` to handle registration, logging in, and logging out processes
   - `base_template.html` to display the username of the logged-in member. If the user is logged in, the human icon, when clicked, logs the user out
   - `base_template.html` to make the human icon redirect the user to the login page (if they are not logged in already)

### Testing & Project Management - Irving Reyes Bravo

**ADDED**
   - **UserRegistrationLogin** to check if a user is able to have their information successfully stored in the system & then log in
   - **UserLogoutTest** to see is a user can log out
   - **UserFailSafe** to see if a logged in user will be redirected back to the home page if they try to access the register link
   - **QuizSessionTrackingTest** to track session data
   - **QuestionPoolTest** for question pool consistency

**UPDATED**
   - Zenhub for this sprint

### Word of the Day - Naomi Rodriguez

**ADDED**
   - installed requests and updates `requirements.txt`
   - Random Words API in order to fetch a random word in Spanish as well as its English translation. Also supports Dutch, French, Chinese, Japanese, and Turkish
   - `word_of_the_day.html` and the ability to redirect to this page from the navbar

**UPDATED**
   - `views.py` to handle user input for word of the day as well as word generation & translation
   - `urls.py` to include paths for word of the day
   - `base_template.html` to display the word of the day icon. Currently appears at all times for testing

### Quiz Templates - Christopher Romo

**ADDED** 
   - quiz url (linked to play button), quiz_correct url, quiz_incorrect url, quiz_recap url
   - quiz view (linked to play button), quiz_correct view, quiz_incorrect view, quiz_recap view
   - `quiz_question.html` (linked to play button), `quiz_correct.html`, `quiz_incorrect.html`, `quiz_recap.html` 
   - splash screen block in `base_template.html`
   - navbar block in `base_template.html`
   - new general navbar in `base_template.html`

**UPDATED**
   - "static/images/", "static/`styles.css`" to: "static/home/images/", "static/home/css/`styles.css`"
   - all {% static %} tags to match new file hierarchy
   - all <style></style> tags have been moved to `styles.css`
   - splash screen functionality is now in splash screen block in `index.html`
   - navbar in navbar block in `index.html`

---
## Sprint 2 (10/29/2024)

### Quiz Logic Bug Fixing - Darion Badillo

**UPDATED**
   - Adjusted AI prompting and AI logic overall
      - Combined both functions into one function
      - Parsing logic/regex updated
      - AI now gives more than just questions. (sentences, phrases, questions, words, etc)
      - Also generates title and description
   - Fixed Next Quiz logic. The button becomes active only when a quiz is generated or not completed
   - Added attributes to the Quiz model for tracking
      - is_completed: boolean
      - score: int
   - Fixed quiz_recap view to work correctly (reset score and start quiz again or finalize score and return to `index.html`)

### Account Streaks - Andrew Douangprachanh

**ADDED**
   - django-apscheduler: Enables scheduling of tasks to run at specified times
      - Updated requirements.txt to include this new package
      - Package link
   - `scheduler.py`: Contains code to initiate the background process that resets streaks
      - Schedules a daily midnight job to reset streak information
      - If the server is shut off and it is turned on the next day, it force runs the reset streak function
   - `tasks.py`: The only task in this file is the one that contains the logic to reset streak information for users. Executes every day at midnight
   - a new model called LastStreakReset to record the last streak reset time, accommodating server downtime

**UPDATED**
   - the Member model to hold streak information such as if they have completed a quiz for the day and the current streak count
   - the home page view to display user streak data when logged in
   - `index.html` to display the streak count when it is greater than 0
   - `apps.py`: Added code to start scheduler.py to run whenever the app starts
   - `tests.py`: Added new tests to ensure that the streak reset function works properly and adjusts the database as needed

### Testing & Project Management - Irving Reyes Bravo

**ADDED**
   - **UserRegistrationLogin** to check if a user is able to have their information successfully stored in the system & then log in
   - **UserLogoutTest** to see is a user can log out
   - **UserFailSafe** to see if a logged in user will be redirected back to the home page if they try to access the register link
   - **QuizTests** to verify that the quiz is generated correctly with the expected attributes and completed by the logged-in user
   - **ResetStreakTests** to verify that daily streak implementation properly resets
   - **WordOfTheDay** to check if a user can access the word of the day
   - **SetLanguageTest** to see if user can select a language to learn

**UPDATED**
   - Zenhub for this sprint

### Language Implementation - Naomi Rodriguez

**ADDED**
   - Javascript to update the flag image to selected language
   - Javascript to store language selection
   - set_language to store the selected language in the user's session and returns a JSON response

**UPDATED**
   - static Spanish flag image to dropdown selection
   - generate_quiz view to use selected language rather than a hardcoded language. Also now uses a selected difficulty rather than a hardcoded one
   - word_of_the_day view to use selected language rather than a hard coded one
   - added set_language path
   - updated `word_of_the_day.html` to verify language selection has been successful

### AI Integration - Christopher Romo

**ADDED**
   - `services.py` (new file to handle open AI logic)
   - generate_translation_questions function (prompts open AI to generate ten questions based on a number of incoming parameters such as difficulty, source language, etc.)
   - translate_sentence function (prompts open AI to translate the incoming phrase to the base language)
   - open AI organization (invited all teammates to join the organization so they can all have API keys and added $15 worth of credits so that we can all test the AI)

**UPDATED**
   - `quiz_recap.html` to include a home button (button takes you to index for better flow)
   - generate_quiz view in `views.py` (added logic to incorporate the new functions in services.py) (now generates questions using open AI) (uses a loop to translate each sentence, create a question object for each, and adds those objects to a quiz object)

---
## Sprint 3 (11/12/2024)

### Index Overhaul - Darion Badillo & Christopher Romo

**ADDED**
   - `quiz_start.html`
      - Serves as a quiz recap page before starting
      - Provides a rundown of quiz settings, including:
         - Quiz Title
         - Quiz Description
         - Difficulty Level
         - Number of Questions
         - Quiz Goal
      - Includes a "Start Quiz" button that takes you to the first question of the quiz

**UPDATED**
   - Index Card is now more user-friendly with additional options:
      - Difficulty selection is now available in the index card
      - Length of Quiz can be selected within the index card
      - Goal of Quiz can be specified directly in the index card
      - Play Button now acts as a "Confirm" button
      - Clicking the Play Button now redirects you to the new `quiz_start.html` page

### Account Pages - Andrew Douangprachanh

**ADDED**
   - `account_details.html`: This page displays the logged-in user's information and allows them to edit details such as username, first name, last name, and email

**UPDATED**
   - `models.py`: Added two new fields to the Member model: dateJoined and longestStreak
   - `views.py`: Added a new view called update_account_details that updates the fields modified by the user on their account details page
   - quiz recap view: Added logic for calculating the longest streak
   - `urls.py`: Added a URL for updating account details
   - `index.html`: For logged-in users, a dropdown that allows them to view their profile information or log out

### Quiz Logic Bug Fixing - Irving Reyes Bravo

**ADDED**
   - is_active boolean attribute (new attribute in Quiz model that seperates "saved for later" quizes)
   - quiz_exit function (saves user's currentl session's quiz and redirects them to the homepage)
   - quiz_continue function (prompts user to return to their previously specified quiz)

**UPDATED**
   - quiz_recap view so each specific user's Quiz database is cleared
   - `index.html` & index view function to check whether the user has an active quiz ("Create Quiz" UI changes to "Continue Quiz" UI)
   - `quiz_question.html` to include an "Exit Quiz" button

### Expanded Language Selection - Naomi Rodriguez

**ADDED**
   - Cleaned up `index.html`. Language selection is now it's own section
   - Moved the flag dropdown from `index.html` into it's own html file to clean up code. Updated dropdown menu to be scrollable
   - Ten new flags users can select from
   - get_word_of_the_day function using openai rather than using random words API

**UPDATED**
   - Added Server Side Includes (SSI) to clear up javascript from `index.html`
   - When clicking any of the drop-downs, the flag would disappear. Flag is now fixed once selected
   - word_of_the_day view to work with openai logic

---
## Sprint 4 (12/10/2024)

### Quiz Logic Bug Fixing / flake8 - Darion Badillo

**ADDED**
   - Implemented Quiz Accuracy Feature: Added a feature that awards points for answers that are 90% accurate to the correct answer. The new accuracy check ignores punctuation and handles contractions (e.g., "don't" vs. "do not") to make the evaluation more user-friendly
      - Installed [Levenshtein](https://pypi.org/project/python-Levenshtein/) library to check for answer accuracy in comparisons
      - Installed [Contractions](https://pypi.org/project/contractions/) library to automatically fix contractions such as you're -> you are

**UPDATED**
   - Fixed Continue Quiz Bug: Addressed the logic issues in the continue_quiz view, where the app would pull information from past, already completed quiz that was exited once
   - Resolved Spanish Flag Persistence Issue: Fixed a persistent bug where the Spanish flag failed to display correctly by renaming `Spanish.png` to `spanish.png` for consistency and proper referencing
   - Fixed 96.11% of code smells defined by flake8

### Django REST / Word of the Day - Andrew Douangprachanh

**ADDED**
   - Installed djangorestframework package and updated `requirements.txt` to include it
   - Created `serializers.py` to serialize all fields of the Member, Question, and Quiz models
   - Added viewsets for the Member, Question, and Quiz models in `views.py` to enable CRUD operations through REST APIs
   - Registered API endpoints for members, quizzes, and questions in `urls.py` using DefaultRouter
   - The word of the day is now resets daily at midnight

**UPDATED**
   - `settings.py` to include rest_framework in the INSTALLED_APPS section to enable Django REST Framework
   - Modified **WordOfTheDayTest** to reflect the current structure and modifications in the codebase
   - `models.py`: Created a new model called "WordOfTheDayTracker". It tracks the languages that have been generated for the word of the day for a member as well as whether they have completed the word of the day for a language
   - `views.py`: Modified the "word_of_the_day" view to work with the new model and do tracking
   - `scheduler.py`: Added a new job that calls a function to reset the word of the day trackers everyday at midnight
   - `tasks.py`: Added a new function that goes through all the "member" objects and resets the trackers
   - `index.html`: Streak information now appears on the homepage again

### Testing & Project Management - Irving Reyes Bravo

**ADDED**
   - **User Registration and Login**: Tests user registration and login process
   - **User Logout**: Tests the logout functionality
   - **User Fail-Safe**: Ensures a logged-in user is redirected to the homepage if they try to access the registration page
   - **Account Details Update**: Tests updating account details (e.g., email)
   - **Quiz Generation and Completion**: Tests the generation and completion of quizzes
   - **Quiz Exit and Continuation**: Tests the quiz exit and continuation functionality
   - **Streak Reset**: Tests resetting streaks for users who have or have not completed a quiz
   - **Word of the Day**: Tests the functionality of the Word of the Day feature
   - **Set Language**: Tests that the user successfully changes the selected language in the session
   - **Daily Lesson**: Tests the functionality of the Daily Lesson feature

**UPDATED**
   - Zenhub for this sprint

### Daily Lesson / UI Bug Fixing - Naomi Rodriguez

**ADDED**
   - Seven new lesson templates with images of basic language learning topics
   - templatetags folder to hold translation logic for html
   - Lesson templates responsive to all screen sizes
   - function_name in `services.py` using openai API to translate given words
   - daily_lesson function in `view.py` to select language and translate given words. Templates cycle daily

**UPDATED**
   - Daily Lesson now clickable in the dropdown panel on `index.html`
   - Word of the Day
      - UI modified to match the rest of the application
      - Words cycle daily
   - Splash Screen
      - Responsive to all screen sizes
      - Stripe along the top of the screen now the same color as the splash screen
   - default language set to Arabic for quiz generation, matching the rest of the default options
   - Added an onerror check so that if currentFlag function fails to load, the Arabic flag will appear as default

### UI Updates / Responsiveness / README Overhaul - Christopher Romo

**UPDATED**
   - Navbar to be an OffCanvas Navbar
      - Replacing the word of the day button and account dropdown is a new hamburger menu
      - Account dropdown options have been moved to this offcanvas panel
      - Word of the Day is now accessible from this offcanvas panel
      - Daily Lesson is now accessible from this offcanvas panel
      - Updates when a user is not logged in
      - Only appears on `index.html`
   - Quiz creation card on `index.html`
      - Labels appear next to dropdowns instead of inside
      - Dropdowns and buttons are now rearranged
      - Cards have been updated for users who aren't signed in / users who can continue a quiz
   - App Responsiveness
      - `quiz_start.html`, `quiz_question.html`, `quiz_correct.html`, `quiz_incorrect.html`, and `quiz_recap.html` have been updated to be more responsive with different browsers
      - Cards on these pages have been wrapped in containers
      - Margins are in place so that even if a card grows large, it shouldn't cover the button
   - Minor changes like card size, text alignment
   - "Next Question" text on buttons in `quiz_question.html` has been changed to "Next"
   - README Documentation for our app, making it more readable and informative

---
# ٩( ᐛ)و
