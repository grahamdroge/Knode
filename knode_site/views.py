from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_user(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		return redirect("home")
	else:
		return HttpResponse("Error logging in")

# Log out user
def logout_user(request):
	logout(request)
	return redirect("/signin/")

# Sign in page
def signin(request):
	return render(request, "registration/login.html")

# Sign up page
def signup(request):
	return HttpResponse("This is the sign up page")

@login_required
# Home screen
def home(request):
	return HttpResponse("This is the home page")