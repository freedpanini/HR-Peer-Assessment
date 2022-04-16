from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from courses.models import Course, Registration, Invitation, Team
from .forms import UserRegistrationForm
from itertools import chain


def home_view(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return render(request, 'users/home.html')

def home_view(request):
    """
    #renders users
    #https://stackoverflow.com/questions/36631419/display-data-from-a-database-in-a-html-page-using-django
    """
    if not request.user.is_authenticated:
        return redirect('/login')
    data = {
        "course_list": get_user_registrations(request),
        "invitations": get_user_invitations(request)
    }
    return render(request, 'users/home.html', data)

def surveys_home_view(request, course_pk):
    if not request.user.is_authenticated:
        return redirect('/login')
    data = {
        "course_list": get_user_registrations(request),
        "invitations": get_user_invitations(request),
        "current_course": course_pk,
        "current_course_name": Course.objects.get(course_id=course_pk).name
    }

    return render(request, 'users/surveys_home.html', data)


def users_home_view(request, course_pk):
    if not request.user.is_authenticated:
        return redirect('/login')
    curr = Course.objects.get(course_id=course_pk)

    #locate all student emails registered in the current course
    registrations = Registration.objects.filter(course_id=curr.course_id)
    student_emails = [o.student for o in registrations]

    # Get course teams
    teams = Team.objects.filter(course_id=curr.course_id)

    #locate all user objects associated with registered students
    students = User.objects.filter(email__in = student_emails)

    for i in range(len(teams)):
        team_students = registrations.filter(team_id=teams[i].team_id).values_list('student')
        teams[i].students = students.filter(email__in = team_students)


    data = {
        "course_list": get_user_registrations(request),
        "invitations": get_user_invitations(request),
        "current_course": course_pk,
        "students": students,
        "current_course_name": curr.name,
        "teams": teams
    }

    return render(request, 'users/users_home.html', data)

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
        return redirect('home')
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

def get_user_registrations(request):
    if request.user.is_staff:
        registrations = Course.objects.filter(professor=request.user.email)
    else:
        registrations = Registration.objects.filter(student=request.user.email)
    return registrations

def get_user_invitations(request):
    invitations = []
    if not request.user.is_staff:
        invitations = Invitation.objects.filter(student=request.user.email)
    return invitations
