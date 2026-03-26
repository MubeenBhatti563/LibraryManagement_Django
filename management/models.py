from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver
from datetime import timedelta
import os
import uuid

# Create your models here.
def get_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    # This automatically picks the right folder based on the model
    if isinstance(instance, Student):
        return os.path.join('students/', filename)
    return os.path.join('books/', filename)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_no = models.CharField(max_length=50, unique=True)
    contact_no = models.CharField(max_length=15, unique=True)
    profile_img = models.ImageField(upload_to=get_upload_path, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Book(models.Model):
    title = models.CharField(max_length=200) 
    isbn = models.CharField(max_length=13, unique=True)
    total_copies = models.PositiveIntegerField(default=1)
    book_pic = models.ImageField(upload_to=get_upload_path, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class IssuedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    actual_return_date = models.DateField(null=True, blank=True)
    return_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.return_date = timezone.now().date() + timedelta(days=7)
        super().save(*args, **kwargs)

    @property
    def calculate_fine(self):
        # We ensure end_date is always a 'date' object for the math to work
        if self.return_status and self.actual_return_date:
            end_date = self.actual_return_date
        else:
            end_date = timezone.now().date()
            
        if end_date > self.return_date:
            overdue_days = (end_date - self.return_date).days
            return overdue_days * 200
        return 0
    
    def __str__(self):
        return f"{self.book} - {self.student.user.username}"
    
# Signal for deleting physical image too
@receiver(post_delete, sender=Student)
def delete_physical_profile(sender, instance, **kwargs):
    if instance.profile_img:
        if os.path.isfile(instance.profile_img.path):
            os.remove(instance.profile_img.path)

@receiver(post_delete, sender=Book)
def deleet_physical_book(sender, instance, **kwargs):
    if instance.book_pic:
        if os.path.isfile(instance.book_pic.path):
            os.remove(instance.book_pic.path)