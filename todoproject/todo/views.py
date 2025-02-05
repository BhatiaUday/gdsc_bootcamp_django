from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from .forms import SignupForm, TaskForm, CustomPasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth.models import User


# View to display and modify password hash and salt
@login_required
def view_password_hash_and_salt(request):
    user = request.user  # Current logged-in user
    password_hash = user.password  # The hashed password stored in the database

    # Extract salt from the hash (for demonstration purposes)
    salt = password_hash.split('$')[2]  # Extracting salt portion from the password hash

    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # Change the password
            form.save()
            # Update session to keep the user logged in after password change
            update_session_auth_hash(request, form.user)
            success_message = "Your password has been changed successfully!"
        else:
            success_message = None
    else:
        form = CustomPasswordChangeForm(request.user)
        success_message = None

    return render(request, 'todo/view_password_hash_and_salt.html', {
        'password_hash': password_hash,
        'salt': salt,
        'form': form,
        'success_message': success_message
    })


# Home Page
def home(request):
    user_count = User.objects.count()
    return render(request, 'todo/home.html', {'user_count': user_count})

#  Prevent signup if user is logged in
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('todo_list')  # Redirect to tasks page if already logged in

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('todo_list')  # Redirect to tasks page after successful signup
    else:
        form = UserCreationForm()

    return render(request, 'todo/signup.html', {'form': form})

# Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('todo_list')  # Redirect to tasks page if logged in

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('todo_list')  # Redirect to tasks page after login
    else:
        form = AuthenticationForm()

    return render(request, 'todo/login.html', {'form': form})

# Logout
def logout_view(request):
    logout(request)
    return redirect('home')

# To-Do List (Private)
@login_required
def todo_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todo/todo_list.html', {'tasks': tasks})

# To-Do List with Add/Delete Feature
@login_required
def todo_list(request):
    tasks = Task.objects.filter(user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('todo_list')
    else:
        form = TaskForm()

    return render(request, 'todo/todo_list.html', {'tasks': tasks, 'form': form})

# Delete Task
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('todo_list')
