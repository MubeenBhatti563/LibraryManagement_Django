from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_no = models.CharField(max_length=50, unique=True)
    contact_no = models.CharField(max_length=15, unique=True)
    profile_img = models.ImageField(upload_to="profile_pics/", null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Book(models.Model):
    title = models.CharField(max_length=200) 
    isbn = models.CharField(max_length=13, unique=True)
    total_copies = models.PositiveIntegerField(default=1)
    image_pic = models.ImageField(upload_to='books_pics/', null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class IssuedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField()
    return_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.return_date = timezone.now().date() + timedelta(days=7)
        super().save(*args, **kwargs)

    @property
    def calculate_fine(self):
        if not self.return_status and timezone.now().date() > self.return_date:
            overdue_days = (timezone.now().date() - self.return_date).days
            return overdue_days * 200
        return 0
    
    def __str__(self):
        return f"{self.book} - {self.student.user.username}"