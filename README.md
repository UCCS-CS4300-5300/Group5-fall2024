# Group5-fall2024

sprint0-3 completed 9/30/2024 (Tag name - sprint0-3)

'User Registration' (10/14/2024)
-Added the ability for the user to create an account and log in to the website.
-Added two new templates in the "authentication" folder called "login.html" and "register.html"
-Added 'forms.py' which allows for defining a form with information that must be filled by the user to register
-Added 'decorators.py'. So far, only has one decorator that doesn't allow logged in users to access the register and logging in links
-Added pytests to make sure that logging in, logging out, and failsafes work
-Updated 'models.py' to include a new model called "Member" which will represent a singular user. Contains fields such as first and last name.
-Updated 'urls.py' to include links to registration, logging in, and logging out
-Updated 'views.py' to handle registration, logging in, and logging out
-Modified the base template to display the username of the logged in Member. If user is logged in, the human icon, when clicked, logs the user out (temporary).
-Modified the base template to have the human icon redirect user to login page (if not logged in already)
-BUG: The logout view doesn't redirect users back to the homepage, but back to the login page if they log out even though there is logic that says otherwise...