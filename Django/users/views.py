
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm

def home(request):
    return render(request, 'users/home.html')

def login(request):
    return render(request, 'users/login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        print("here")
        if form.is_valid():
            form.save()
            print("success")
            messages.success(request, f'Your account has been created. You can log in now!')    
            return redirect('login')
        else:
            print("form is not valid")
    else:
        form = UserRegistrationForm()
        print("failed")

    context = {'form': form}
    return render(request, 'users/register.html', context)