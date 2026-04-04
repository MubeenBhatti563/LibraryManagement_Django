from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from .models import IssuedBook, Book, Student

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'})
    )

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter Email'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = IssuedBook
        fields = ['student', 'book']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'borrow_input'})
        
        self.fields['book'].queryset = Book.objects.filter(total_copies__gt=0)

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get("student")
        book = cleaned_data.get("book")

        if student:
            active_issues = IssuedBook.objects.filter(student=student, return_status=False)
            # Check Limit
            if active_issues.count() >= 2:
                raise ValidationError("Student has reached the limit of 2 books.")
            
            # Check Duplicate
            if active_issues.filter(book=book).exists():
                raise ValidationError("Student already has this specific book.")
            # Check if copies available
            if book.total_copies < 1:
                raise ValidationError(f"Error: {book.title} is currently out of stock")
      
        return cleaned_data
    
class ReturnBookForm(forms.Form):
    student = forms.ModelChoiceField(
        # Use 'issued_books' because that is your related_name for Student
        queryset=Student.objects.filter(issued_books__return_status=False).distinct(),
        widget=forms.Select(attrs={'class': 'return_input'})
    )
    
    book = forms.ModelChoiceField(
        # Use 'issued_instances' because that is your related_name for Book
        queryset=Book.objects.filter(issued_instances__return_status=False).distinct(),
        widget=forms.Select(attrs={'class': 'return_input'})
    )

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        book = cleaned_data.get('book')

        issue = IssuedBook.objects.filter(student=student, book=book, return_status=False).first()
        if not issue:
            raise forms.ValidationError("No active record found for this student and book!")
        
        cleaned_data['issue_record'] = issue
        return cleaned_data