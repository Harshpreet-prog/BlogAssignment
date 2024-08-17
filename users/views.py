from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect

from .forms import SignUpForm
from .forms import LoginForm


def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('home')  # Replace 'home' with the name of your homepage URL pattern
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Replace 'login' with the name of your login URL pattern
    else:
        form = SignUpForm()
    
    return render(request, 'users/signup.html', {'form': form})






def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')  # Replace 'login' with the name of your login URL pattern
