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


def send_email(request, emails, code, name):
	send_mail(f'You\'ve been added to {name}! ',
	f'Hello there, this is an automated message. You have been added to a new course, course code: {code}. If you do not have an account, use the link below to register! http://127.0.0.1:8000/register/ ',
	'Software Engineer HumanResources',
<<<<<<< HEAD
<<<<<<< HEAD
	['yangalm@bc.edu','panfr@bc.edu','brooksha@bc.edu','crewsz@bc.edu','scottfe@bc.edu','lobanov@bc.edu'],
=======
	[email],
>>>>>>> 15a4e1763f93e27ee50b1e670615c5056c03338a
=======
	emails,
>>>>>>> 4d434110aa2a7c8f0066adaef7bbd64f74fcb8bb
	fail_silently=False)
	return render(request, 'courses/send_email.html',{})

def invite_students(request, data, course_id):
	emails = data['emails']
	if emails is None or len(emails) == 0:
		return
	emails = emails.split(",")
	i = 0
	while i < len(emails):
		emails[i] = emails[i].strip()
		# prevent duplicate invitations
		if Invitation.objects.filter(student=emails[i], course_id=course_id).count() == 0:
			Invitation.objects.create(student=emails[i], course_id=course_id)
		else:
			emails.pop(i)
			i -= 1
		i += 1
	send_email(request, emails, data['code'], data['name'])

def accept_invite(request, student, course_id):
	Invitation.objects.get(student=student, course_id=course_id).delete()
	Registration.objects.create(student=student,course_id=course_id,team_id=0)

def decline_invite(request, student, course_id):
	Invitation.objects.get(student=student, course_id=course_id).delete()