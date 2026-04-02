from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, BorrowBookForm
from .models import Student, IssuedBook, Book

# Create your views here.
def home(request):
    return render(request, "base.html")

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect("home")  # normal full-page redirect
    return render(request, "login.html", {"form": form})

def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()  # create user

        return redirect("login")
    return render(request, "register.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")

def dashboard_view(request):
    return render(request, "Dashboard/dashboard.html")

def student_info(request):
    students = Student.objects.all().select_related('user')
    context = {
        "students": students
    }

    if request.headers.get('HX-Request'):
        return render(request, 'Dashboard/partials/student_info_content.html', context)
    return render(request, 'Dashboard/student_info.html', context)

def statistics(request):
    return render(request, "Dashboard/statistics.html")

def borrow_history(request):
    return render(request, "Dashboard/borrow_history.html")

def return_book(request):
    return render(request, "Dashboard/return_book.html")

def borrow_book(request):
    if request.method == 'POST':
        form = BorrowBookForm(request.POST)
        if form.is_valid():
            issued_book = form.save()
            
            book = issued_book.book
            book.total_copies -= 1
            book.save()

            return redirect('dashboard')
    else:
        form = BorrowBookForm()

    if request.headers.get('HX-Request'):
        return render(request, 'Dashboard/partials/borrow_book.html', {'form': form})
    return render(request, "Dashboard/borrow_book.html", {'form': form})

def available_books(request):
    books = Book.objects.filter(total_copies__gt=0)
    context = {
        "books": books
    }
    
    if request.headers.get('HX-Request'):
        return render(request, "Dashboard/partials/available_books.html", context)
    return render(request, "Dashboard/available_books.html", context)