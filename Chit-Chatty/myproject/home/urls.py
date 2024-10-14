from django.urls import path, include
from . import views

urlpatterns = [
    # Default path (Home)
    path('', views.index, name='index'),

    # Path for registering
    path('register/', views.registerPage, name = 'registration-page'),

    # Path for logging in
    path('login/', views.loginPage, name='login-page'),

    # Path for logging out
    path('logout/', views.logout, name ='logout'),
]