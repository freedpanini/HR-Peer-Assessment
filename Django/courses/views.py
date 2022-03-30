from django.shortcuts import render, redirect
from .models import Course, Team, Invitation, Registration
from .forms import CourseForm, TeamForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
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
	ctx={
		'name':name,
		'code':code,
	}
	message=render_to_string('courses/email.html',ctx)
	send_mail(f'You\'ve been added to {name}! ',
	message,
	settings.EMAIL_HOST_USER,
	emails,
	fail_silently=False,html_message=message)
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