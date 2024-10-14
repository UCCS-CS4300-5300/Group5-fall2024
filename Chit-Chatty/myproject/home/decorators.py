from django.shortcuts import redirect

# Decorator for restricting user access to certain areas if they already logged in 
# Redirects logged in user back to homepage
def unauthenticatedUser(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func