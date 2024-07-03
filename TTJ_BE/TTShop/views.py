import os
import json


from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout as auth_logout
from django.contrib import messages

from rest_framework.response import Response
from rest_framework import status

from .models import User, Profile
from .backends import FirebaseBackend
from .backends import EmailBackend



######################################## Sign-In Methods ########################################### 
@csrf_exempt
def google_signin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_token = data.get('idToken')
        if not id_token:
            return Response({"error": "Access token required"}, status=status.HTTP_400_BAD_REQUEST)
        user = FirebaseBackend().authenticate(request, id_token)
        if user:
            login(request, user, "user.backends.FirebaseBackend")
            return JsonResponse({"detail": "Account created and Logged in successfully"}, status=status.HTTP_200_OK)
        else:
            return HttpResponse('Authentication failed', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return HttpResponse('Google Login')
    

# REGISTER:
@csrf_exempt
def email_register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        full_name = data.get('full_name')
        username = data.get('username')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')
        password2 = data.get('password2')

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "This username is already taken")
                return JsonResponse({"status": 'That username is taken'}, status=400)

            if User.objects.filter(email=email).exists():
                messages.error(request, "This email is already taken")
                return JsonResponse({"status": 'That email is taken'}, status=400)

            
            user = User.objects.create_user(username=username, password = password, email = email)
            profile = Profile.objects.create(user = user, full_name = full_name, phone_number = phone_number)
            user.save()
            login(request, user, 'users.backends.EmailBackend')


            return JsonResponse({"status": "User registered successfully"})
        else:
            return JsonResponse({"status": 'Passwords do not match'}, status=400)
    else:
        return HttpResponse("Register")
    
#LOGIN:
@csrf_exempt
def email_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        user = EmailBackend().authenticate(request = request, email = email, password = password)
        print(user)
        if user is not None:
            login(request, user, 'user.backends.EmailBackend')
            messages.success(request, 'You are now logged in')
            return JsonResponse({"status" : "You are now login"}, status = 200)
        else:
            messages.error(request, "no user")
            return JsonResponse(
                {"status": "Invalid credentials"},
                status=403
            )
    else:
        return HttpResponse("Login")
    

# LOGOUT
@csrf_exempt
def logout(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse(
                {"status": "Unauthenticated"},
                status=400
            )
        auth_logout(request)
        messages.success(request, "You are now logged out")
        return JsonResponse(
            {"status": "You are now logged out"},
            status=200
        )
    else:
        return HttpResponse("Logout")
