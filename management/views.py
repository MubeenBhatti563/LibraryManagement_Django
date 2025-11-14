from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

# Create your views here.
def home(request):
    return render(request, "base.html")

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.headers.get("HX-Request") == "true":
                return redirect("home")
    return render(request, "login.html", {"form": form})

def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            if request.headers.get("HX-Request") == "true":
                return redirect("login")
    context = {"form": form}
    template = "register.html"
    return render(request, template, context)

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")