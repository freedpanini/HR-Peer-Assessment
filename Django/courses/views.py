from django.shortcuts import render, redirect
from .models import Course, Team, StudentTeam
from .forms import CourseForm, TeamForm
from django.core.mail import send_mail
# Create your views here.
def course_creation_view(request):
	# form = CourseForm(request.POST or None)
	# if form.is_valid():
	# 	print("Form is valid")
	# 	Course.objects.create(**form.cleaned_data)
	# 	form.save()
	# else:
	# 	print("ERRORS")
	# 	print(form.errors)
	
	# if request.method == "POST":
	# 	name = request.POST.get('name')
	# 	semester = request.POST.get('semester')
	# 	year = request.POST.get('year')
	# 	code = request.POST.get('code')
	# 	num_teams = request.POST.get('num_teams')
	# 	Course.objects.create(name=name, semester=semester, year=year, code=code)

	form = CourseForm()
	if request.method == "POST":
		form = CourseForm(request.POST)
		if form.is_valid():
			Course.objects.create(**form.cleaned_data)
			return redirect('adminhome')

	context = {'form':form}
	return render(request, "courses/course_create.html", context)


def team_creation_view(request):
	form=TeamForm()
	if request.method=="POST":
		form=TeamForm(request.POST)
		if form.is_valid():
			Team.objects.create(**form.cleaned_data)
			form=TeamForm()
	context={'form':form}
	print('ALAHLALJLAJLKSJD')
	redirect('send_email')
	return render(request, "courses/team_create_test.html", context)


def send_email(request):
	send_mail('You\'ve been added to a new course! ',
	'Hello there, this is an automated message. You have been added to a new course, the course code has been provided below. If you do not have an account, use the link below to register! http://127.0.0.1:8000/register/ ',
	'Software Engineer HumanResources',
	['yangalm@bc.edu'],
	fail_silently=False)
	return render(request, 'courses/send_email.html',{})
