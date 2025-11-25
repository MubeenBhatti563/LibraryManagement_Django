from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

# Create your views here.
def home(request):
    return render(request, "base.html")

from django.http import HttpResponse

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if request.headers.get("HX-Request") == "true":
                response = HttpResponse()
                response['HX-Redirect'] = '/home/'  # or use reverse('dashboard')
                return response

            return redirect("home")  # normal full-page redirect
    return render(request, "login.html", {"form": form})

def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()  # create user

        if request.headers.get("HX-Request") == "true":
            response = HttpResponse()
            response['HX-Redirect'] = reverse("login")
            return response

        return redirect("login")

    return render(request, "register.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")

def dashboard_view(request):
    return render(request, "Dashboard/dashboard.html")

def student_info(request):
    return render(request, "Dashboard/student_info.html")

def statistics(request):
    return render(request, "Dashboard/statistics.html")

def borrow_history(request):
    return render(request, "Dashboard/borrow_history.html")

def return_book(request):
    return render(request, "Dashboard/return_book.html")

def available_books(request):
    return render(request, "Dashboard/available_books.html")