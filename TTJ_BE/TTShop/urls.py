from django.urls import path
from . import views



urlpatterns = [
    path("google-signin/", views.google_signin),
    path("email-signin/", views.email_login),
    path("email-register/", views.email_register),
    path("logout/", views.logout)
]