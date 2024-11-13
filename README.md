# Group5-fall2024
# ChitChatty Language Learning Application

## Overview

**ChitChatty** is a language learning platform designed to help users improve their language skills through quizzes and dynamic content generation. The app integrates AI tools to generate translation questions and leverages the Googletrans library for handling multiple languages. The app aims to provide an engaging and personalized learning experience by adapting quiz difficulty and user progress.

## Features

### 1. **Dynamic AI Quiz Generation**
   - Store generated and translated questions in a database.
   - FUTURE Support for multiple languages, with the ability to set source and target languages.

### 2. **User Authentication**
   - User registration, login, and session management.
   - Users can generate personalized quizzes based on selected difficulty.

### 3. **Customizable Difficulty**
   - Three difficulty levels: Easy, Medium, and Hard.
   - Users can choose difficulty levels from a dropdown menu in the navbar.
   - Each quiz adapts its content based on the selected difficulty.

### 4. **Quiz Management**
   - Track user progress during quizzes.
   - Maintain session data for correct and incorrect answers.
   - Display feedback based on user performance.

### 5. **Quiz Recap**
   - Display the user’s score at the end of each quiz.
   - Recap page provides a summary of the quiz, including correct and incorrect answers and overall performance.

### 6. **Frontend UI**
   - Clean and user-friendly interface with Bootstrap-based styling.
   - Dynamic scaling Play button that provides a smooth, interactive experience.
   - Play button lifts upon hover to create a sense of depth.
   - Active quiz indicator that enables or disables the Play button based on quiz availability.



## Installation

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

4. Load the sample data:

   ```bash
   python manage.py add_questions
   ```

5. Run the server:

   ```bash
   python manage.py runserver
   ```

6. Access the app at `http://127.0.0.1:8000`.

---

## Future Features

- **Goal-based Learning**: A dropdown to select specific learning goals (e.g., travel, fluency) and generate quizzes based on these goals.
- **Expanded Language Support**: Adding more languages and improving translation accuracy.

---

## Updates

### Quiz Streaks and AI Integration (10/28/2024)

We've upgraded ChitChatty with AI-powered quiz generation and a streak tracking system, enhancing both personalization and motivation.

#### Key Changes:
- **Dynamic Quiz Generation**: AI-generated question-answer pairs with titles and descriptions, adapting content based on difficulty level.

- **New Feature: Quiz Streaks**
   - Streaks increment daily when a user completes a quiz.
   - Resets automatically everyday at midnight.

- **New Package: `django-apscheduler`**
   - Enables scheduling of tasks to run at specified times.
   - Updated `requirements.txt` to include this new package.
   - [Package link ](https://pypi.org/project/django-apscheduler/)

- **New file: `services.py`**
   - Handles all openai prompts and parses the response from it


- **New file: `scheduler.py`**
   - Contains code to initiate the background process that resets streaks.
   - Schedules a daily midnight job to reset streak information.
   - If the server was shut off and it is turned on the next day, it force runs the reset streak function!

- **New file: `tasks.py`**
   - The only task in this file is the one that contains the logic to reset streak information for users. Executes everyday at midnight.

- **Model Adjustments**
   - Modified the `Member` model to hold streak information such as if they have completed a quiz for the day and the current streak count.
   - Created a new model called `LastStreakReset` to record the last streak reset time, accommodating server downtime.

- **View Adjustments**
   - Updated the home page view to display user streak data when logged in.

- **HTML Adjustments**
   - Modified `index.html` to display the streak count when it is greater than 0

- **Modified `apps.py`**
   - Added code to start `scheduler.py` to run whenever the app starts

- **Modified `tests.py`**
   - Added new tests to ensure that the streak reset function works properly and adjusts the database as needed


#### Bug Fixes 

In this update, we addressed key bugs to improve ChitChatty’s functionality:

- **Login Check for Quiz Generation**: The difficulty selection now verifies if a user is logged in. If not, it redirects to the login page.
- **Next Quiz Logic**: Ensured that the “Next Quiz” button only activates for uncompleted quizzes and restricted multiple quiz generation until the current quiz is complete.
- **Quiz Model Enhancements**: Added `is_completed` and `score` attributes for more precise quiz tracking.
- **Quiz Recap Logic**: Adjusted the recap view to reset or finalize the quiz based on user selection.
---


### **October 17, 2024**

#### Implemented Features and Fixes
- **Quiz and Question Models**
   - Adjusted the `Quiz` model to include a boolean `is_next` flag to indicate the next quiz.
   - Created the `Question` model with the following fields:
     - Foreign key to `Quiz`.
     - `translation_question` to hold the source language phrase.
     - `correct_answer` to store the correct translation.
     - `source_language` and `target_language` fields.
     - `difficulty` to categorize questions into Easy, Medium, or Hard.
   - Created a M:N relationship between quizzes and generated questions.

- **Management/Commands**
   - Created the `Management/Commands` directory to manage dynamic question loading.
   - Implemented a command that adds 30 translation questions (10 for each difficulty) into the database.

- **View Adjustments**
   - Moved all quiz templates into a newly created `quiz` folder under `templates`.
   - Filled out views for quiz operations including `quiz`, `quiz_recap`, `quiz_correct`, `quiz_incorrect`, and `next_question`.
   - Implemented the `next_question` view to handle question progression.
   - Adjusted the `generate_quiz` view to handle dynamic quiz generation based on difficulty.
   - Fixed how question IDs are linked to quizzes to prevent the same question from being displayed repeatedly.

- **Quiz Recap and Progress**
   - Created a `quiz_recap` template and view that provides a recap of quiz performance.
   - Handled session variables for quiz progress (`correct_count`, `incorrect_count`, `question_id`) to ensure smooth tracking of user performance.

- **Random Feedback**
   - Added pools of positive and negative feedback in the `quiz_correct` and `quiz_incorrect` views to display random feedback after each question.

- **Styling Improvements**
   - Hid the "Goal" dropdown in the navbar for now, as that feature is pending future development.
   - Ensured the Play button has a consistent 3D appearance with enhanced depth and shadows for better visual feedback.

- **Navbar Dropdown Menus**
   - The dropdown menus in the navbar no longer hover or float unintentionally.
   - Dropdown selections are now properly displayed, reflecting the chosen difficulty level.
   
- **Play Button**
   - Separated the Play button styling from other items in the `styles.css` file.
   - Fixed the hover behavior of the Play button to lift up instead of enlarging.
   - Made the Play button dynamically scale when active and ensured it remains aligned with the card element.
   - Disabled the Play button if no quiz is available.
---
sprint0-3 completed 9/30/2024 (Tag name - sprint0-3)

### Feature Added: User Registration (10/14/2024)

- **Added** the ability for the user to create an account and log in to the website.
- **Added** two new templates in the "authentication" folder called `login.html` and `register.html`.
- **Added** `forms.py`, which allows for defining a form with information that must be filled by the user to register.
- **Added** `decorators.py`. So far, it only has one decorator that prevents logged-in users from accessing the registration and login links.
- **Added** pytests to ensure that logging in, logging out, and failsafes work correctly.
- **Updated** `models.py` to include a new model called "Member," which represents a single user and contains fields such as first and last name.
- **Updated** `urls.py` to include links for registration, logging in, and logging out.
- **Updated** `views.py` to handle registration, logging in, and logging out processes.
- **Modified** the base template to display the username of the logged-in member. If the user is logged in, the human icon, when clicked, logs the user out (for now).
- **Modified** the base template to make the human icon redirect the user to the login page (if they are not logged in already).
- **BUG**: The logout view doesn't redirect users back to the homepage but instead to the login page, even though there is logic that states otherwise...

---
### Feature Added: Word of the Day
- **Added** installed requests and updates requirements.txt
- **Added** `Random Words API` in order to fetch a random word in `Spanish` as well as its `English` translation. Also supports `Dutch, French, Chinese, Japanese, and Turkish`.
- **Added** `word_of_the_day.html` and the ability to redirect to this page from the navbar.
- **Updated** `views.py` to handle user input for word of the day as well as word generation & translation
- **Updated** `urls.py` to include paths for word of the day
- **Modified** the base template to display the word of the day icon. Currently appears at all times for testing. Eventually will only be clickable once a day.

***
### Feature Added: Language Selection
***

`index.html`
- *Flag image on top left corner now dynamic. Click to open a dropdown menu to select language to learn. When a language is selected, the flag will update and display the language the user has selected.*

**Modified**: static Spanish flag image to dropdown selection
**Added**: Javascript to update the flag image to selected language
**Added**: Javascript to store language selection

`views.py`
**Modified**: `generate_quiz` to use selected language rather than a hardcoded language. Also now uses a selected difficulty rather than a hardcoded one.
**Modified**: `word_of_the_day` to use selected language rather than a hard coded one.
**Added**: `set_language` to store the selected language in the user's session and returns a JSON response.

`urls.py`
**Modified**: added `set_language` path

`word_of_the_day.html`
**Modified**: updated to verify language selection has been successful

**Error fixed**: `UnicodeEncodeError` fixed in `services.py`
***
### Future Features
***
**LibreTranslate API**
- Add more languages by implementing an API to translate English sentences. Supports 34 languages.

---

### Updated: Language Selection Extended
`settings.py`
- **Modified**: Added Server Side Includes (SSI) to clear up javascript from `index.html`. 

`language_selection.html`
- **Added**: Cleaned up `index.html`. Language selection is now it's own section.

`templates`
- **Added**: `language_selection.html`. Moved the flag dropdown from `index.html` into it's own html file to clean up code. Updated dropdown menu to be scrollable.
- **Added**: Ten new flags users can select from.
- **Fixed**: When clicking any of the drop-downs, the flag would disappear. Flag is now fixed once selected.

`services.py`
- **Added**: `get_word_of_the_day` function using openai rather than using random words API.

`views.py`
- **Modified**: `word_of_the_day` to work with openai logic

---

### Feature Added: Templates (10/14/2024)
urls.py
- **Added** quiz url (linked to play button)
- **Added** quiz_correct url
- **Added** quiz_incorrect url
- **Added** quiz_recap url

views.py
- **Added** quiz view (linked to play button)
- **Added** quiz_correct view
- **Added** quiz_incorrect view
- **Added** quiz_recap view

templates
- **Added** quiz_question.html (linked to play button) (complete)
- **Added** quiz_correct.html (complete)
- **Added** quiz_incorrect.html (complete)
- **Added** quiz_recap.html (complete)

- **Changed:** "static/images/", "static/styles.css"
	to: "static/home/images/", "static/home/css/styles.css"

- **Changed:** all {% static %} tags to match new file heirarchy

- **Moved** all <style></style> to styles.css

navbar/splash screen changes
- **Added** splash screen block in base.html
- **Added** navbar block in base.html
- **Added** new general navbar in base.html

- **Moved** splash screen functionality to splash screen block in index.html
- **Changed** navbar in navbar block in index.html
  
---

### Feature Added: AI Integration (10/25/2024)
**ADDED**
- services.py (new file to handle open AI logic)
- generate_translation_questions function (prompts open AI to generate ten questions based on a number of incoming parameters such as difficulty, source language, etc.)
- translate_sentence function (prompts open AI to translate the incoming phrase to the base language)
- open AI organization (invited all teammates to join the organization so they can all have API keys and added $15 worth of credits so that we can all test the AI)

**UPDATES**
- updated quiz_recap template to include a home button (button takes you to index for better flow)
- updated generate_quiz view in views.py (added logic to incorporate the new functions in services.py) (now generates questions using open AI) (uses a loop to translate each sentence, create a question object for each, and adds those objects to a quiz object)

---

### Feature Added: Quiz Continuation (11/12/2024)
**ADDED**
- is_active boolean attribute (new attribute in Quiz model that seperates "saved for later" quizes)
- quiz_exit function (saves user's currentl session's quiz and redirects them to the homepage)
- quiz_continue function (prompts user to return to their previously specified quiz)

**UPDATES**
- updated quiz_recap view so each specific user's Quiz database is cleared
- updated index.html & index view function to check whether the user has an active quiz ("Create Quiz" UI changes to "Continue Quiz" UI)
- updated quiz_question.html to include an "Exit Quiz" button

**LIMITS**
- while a user can return to their specified quiz, they cannot return to the question they exited from [AS OF YET]


---
#### Testing Functions (15 in total)
1. UserRegistrationLogin
	Purpose: Tests user registration and login process.
	Steps:
	Registers a user with provided credentials.
	Logs the user in and verifies successful redirection to the homepage.
2. UserLogoutTest
	Purpose: Tests the logout functionality.
	Steps:
	Logs in a user, then verifies they are logged out and redirected to the homepage.
3. UserFailSafe
	Purpose: Ensures a logged-in user is redirected to the homepage if they try to access the registration page.
	Steps:
	Logs in a user and tries to access the registration page.
	Verifies they are redirected back to the homepage.
4. AccountDetailsTest
	Purpose: Tests updating account details (e.g., email).
	Steps:
	Loads the account details page.
	Updates the email field and verifies the changes are saved and reflected on the account page.
5. QuizTests
	Purpose: Tests the generation and completion of quizzes.
	Steps:
	Generates a quiz with specific parameters (difficulty, number of questions).
	Verifies the quiz is created and contains questions.
	Completes the quiz and checks if streaks are updated and the quiz is marked as completed.
6. QuizExitAndContinueTests
	Purpose: Tests the quiz exit and continuation functionality.
	Steps:
	Exits an ongoing quiz and verifies the quiz status.
	Verifies that the option to continue the quiz is available on the homepage.
7. ResetStreakTests
	Purpose: Tests resetting streaks for users who have or have not completed a quiz.
	Steps:
	Resets streaks for users who haven’t completed a quiz.
	Verifies that streaks are reset and that users who have completed quizzes retain their streaks.
8. WordOfTheDayTest
	Purpose: Tests the functionality of the Word of the Day feature.
	Steps:
	Verifies the correct display of the Word of the Day and its translation.
	Tests the user's ability to correctly guess the word and receive feedback.
	Verifies the session is cleared after a correct guess.
