# Group5-fall2024
# ChitChatty Language Learning Application

## Overview

**ChitChatty** is a language learning platform designed to help users improve their language skills through quizzes and dynamic content generation. The app integrates AI tools to generate translation questions and leverages the Googletrans library for handling multiple languages. The app aims to provide an engaging and personalized learning experience by adapting quiz difficulty and user progress.

## Features

### 1. **Dynamic Quiz Generation**
   - Store generated and translated questions in a database.
   - Support for multiple languages, with the ability to set source and target languages.

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

### 7. **Question Pool**
   - 30 questions preloaded into the app, with 10 questions available for each difficulty level.
   - Questions cover basic translation phrases and vocabulary.


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
- **AI Integration** for an even more dynamic quiz generation
- **Expanded Language Support**: Adding more languages and improving translation accuracy.

---

## Updates

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
- **Added** `word_of_the_day.html`
