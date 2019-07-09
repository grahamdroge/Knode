from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Sign in page
def signin(request):
	return render(request, "registration/login.html")

# Sign up page
def signup(request):
	return HttpResponse("This is the sign up page")

@login_required
# Home screen
def home(request):

	return render(request, "knode_site/home.html")