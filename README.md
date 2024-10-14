# Group5-fall2024

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