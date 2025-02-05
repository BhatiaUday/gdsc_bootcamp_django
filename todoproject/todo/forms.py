from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Task


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a new task...'}),
        }
        
class CustomPasswordChangeForm(PasswordChangeForm):
    """This form is used to change the password and update hash & salt."""

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
