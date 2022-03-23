from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm

def home_view(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return render(request, 'users/home.html')

def admin_home_view(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return render(request, 'users/adminhome.html')

def student_home_view(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return render(request, 'users/studenthome.html')

def assessment_view(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return render(request, 'users/peer-assessment.html')

def summary_view(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return render(request, 'users/assessment-results.html')

def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if user.is_staff:
            return redirect('adminhome') #redirects to home
        else:
            return redirect('studenthome')
    else:
        if request.method != 'GET':
            print('did not work')
            messages.error(request, f'Incorrect username or password')  
        return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
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
            print(form.errors)
    else:
        form = UserRegistrationForm()
        print("failed")

    context = {'form': form}
    return render(request, 'users/register.html', context)