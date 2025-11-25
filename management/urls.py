from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("login/", views.login_view, name='login'),
    path("register/", views.register, name='register'),
    path("logout/", views.logout_view, name='logout'),
    path("dashboard/", views.dashboard_view, name='dashboard'),
    path("dashboard/student-info/", views.student_info, name="student_info"),
    path("dashboard/statistics/", views.statistics, name="statistics"),
    path("dashboard/borrow-history/", views.borrow_history, name="borrow_history"),
    path("dashboard/return-book/", views.return_book, name="return_book"),
    path("dashboard/available-books/", views.available_books, name="available_books"),
]
