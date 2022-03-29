from django.shortcuts import render, redirect
from .models import Course, Team, Invitation, Registration
from .forms import CourseForm, TeamForm
from django.core.mail import send_mail
# Create your views here.
def course_creation_view(request):
	form = CourseForm()
	if request.method == "POST":
		form = CourseForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			course_id = Course.objects.create(name=data['name'],semester=data['semester'],year=data['year'],code=data['code']).course_id
			invite_students(request, data, course_id)
			return redirect('adminhome')

	context = {'form':form}
	return render(request, "courses/course_create.html", context)


def team_creation_view(request):
	form=TeamForm()
	if request.method=="POST":
		teamname=request.POST.get('teamname')
		
		form=TeamForm(request.POST)
		if form.is_valid():
			Team.objects.create(**form.cleaned_data)
			return redirect('send_email')
			
	context={'form':form}
	return render(request, "courses/team_create.html", context)


def send_email(request, email, code, name):
	send_mail(f'You\'ve been added to {name}! ',
	f'Hello there, this is an automated message. You have been added to a new course, course code: {code}. If you do not have an account, use the link below to register! http://127.0.0.1:8000/register/ ',
	'Software Engineer HumanResources',
	[email],
	fail_silently=False)
	return render(request, 'courses/send_email.html',{})

def invite_students(request, data, course_id):
	emails = data['emails']
	if emails is None or len(emails) == 0:
		return
	emails = emails.split(",")
	for email in emails:
		email = email.strip()
		print(f"Creating invitation for student {email} for course {course_id}")
		Invitation.objects.create(student=email, course_id=course_id)
		print(f"Sending email to {email}")
		send_email(request, email, data['code'], data['name'])
