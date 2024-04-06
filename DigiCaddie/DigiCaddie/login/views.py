from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import login_form, reg_form
from main_page.forms import user_profile_pic_form
from main_page.models import user_information

def index(request):
    # login page for the user
    form = login_form()
    if request.user.is_authenticated:
        return HttpResponseRedirect('/mainpage')
    if request.method == "POST":
        form = login_form(request.POST)
        if 'sign_up' in request.POST:
            return HttpResponseRedirect('/signup')
        if form.is_valid():
            # clean the data and make sure it matches in the database
            u_name = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=u_name, password=password)
            if user is not None:
                # login and move the user to the main page
                login(request, user)
                return HttpResponseRedirect('/mainpage')
            else:
                # bad password or user name
                messages.add_message(request, messages.INFO, "Error username or password do match any account")
    return render(request, "login/index.html", {"form": form})

def logout_user(request):
    # logout the user and move them into the login page
    logout(request)
    return HttpResponseRedirect('/') 


def signup(request):
    form = reg_form()
    if request.POST:
        form = reg_form(request.POST)
        if 'sign_in' in request.POST:
            return HttpResponseRedirect('/')
        # clean all inputs from user and make sure there valid
        if form.is_valid():
                if form.cleaned_data["firstname"] == "" or form.cleaned_data["lastname"] == "":
                    messages.add_message(request, messages.INFO, "Error Please enter a first and last name! Please try again")
                    return render(request, "login/signup.html", {"form": form})                
                if form.cleaned_data["username"] == "":
                    messages.add_message(request, messages.INFO, "Error Please enter a username! Please try again")
                    return render(request, "login/signup.html", {"form": form})
                if User.objects.filter(username = form.cleaned_data["username"]):
                    messages.add_message(request, messages.INFO, "Error username already taken")
                    return render(request, "login/signup.html", {"form": form})
                if form.cleaned_data["email"] == "":
                    messages.add_message(request, messages.INFO, "Error Please enter a email! Please try again")
                    return render(request, "login/signup.html", {"form": form})
                if User.objects.filter(email = form.cleaned_data["email"]):
                    messages.add_message(request, messages.INFO, "Error email already taken")
                    return render(request, "login/signup.html", {"form": form})
                if form.cleaned_data["password"] == "":
                    messages.add_message(request, messages.INFO, "Error no password enterd! Please try again")
                    return render(request, "login/signup.html", {"form": form})
                if form.cleaned_data["password"] != form.cleaned_data["confirm_password"]:
                    messages.add_message(request, messages.INFO, "Error Passwords do not match! Please try again")
                    return render(request, "login/signup.html", {"form": form})
                newacc = User.objects.create_user(form.cleaned_data["username"], form.cleaned_data["email"], form.cleaned_data["password"])
                newacc.first_name = form.cleaned_data["firstname"]
                newacc.last_name = form.cleaned_data["lastname"]
                newacc.save()
                return HttpResponseRedirect('/')
    else:
        return render(request, "login/signup.html", {"form": form})


def good_login(request):
    return render(request, "mainpage.html")