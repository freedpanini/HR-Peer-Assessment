from django.shortcuts import render, redirect
from .models import Course, Team, Invitation, Registration
from .forms import CourseForm, TeamForm, TeamSwapForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from users.views import get_user_invitations, get_user_registrations
from django.contrib.auth.models import User

# Create your views here.
def course_creation_view(request):
	form = CourseForm()
	if request.method == "POST":
		form = CourseForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			course_id = Course.objects.create(name=data['name'],semester=data['semester'],year=data['year'],code=data['code'],professor=request.user.email).course_id
			Team.objects.create(team_name="Default Team",team_num=0,course_id=course_id)
			invite_students(request, data, course_id, data['name'])
			return redirect('home')

	context = {'form':form}
	return render(request, "courses/course_create.html", context)


def team_creation_view(request, course_pk):
	form=TeamForm()
	if request.method=="POST":
		form=TeamForm(request.POST)
		if form.is_valid():
			current_num_teams = len(Team.objects.filter(course_id=course_pk))
			Team.objects.create(team_name=request.POST['team_name'], course_id=course_pk, team_num=current_num_teams)
			return redirect('../users')
	registrations = Registration.objects.filter(course_id=course_pk)
	course_emails = [r.student for r in registrations]
	students = User.objects.filter(email__in = course_emails)
	context = {
				'form':form,
				'students':students
			}
	return render(request, "courses/team_create.html", context)

def team_swap_view(request, course_pk, student_id):
	form = TeamSwapForm()
	if request.method == "POST":
		form=TeamSwapForm(request.POST)
		if form.is_valid():
			switch_team(request,request.POST['student'],course_pk,request.POST['team_id'])
			return redirect('../../users')
	registrations = Registration.objects.filter(course_id=course_pk)
	student_emails = registrations.values_list('student')

	students = User.objects.filter(email__in=student_emails)
	teams = Team.objects.filter(course_id=course_pk)

	selected_student = students.get(id=student_id)
	for i in range(len(students)):
		if students[i] == selected_student:
			students[i].selected = True

	selected_student_team = registrations.get(student=selected_student.email).team_id
	for i in range(len(teams)):
		if teams[i].team_id == selected_student_team:
			teams[i].selected = True

	context = {
				'form':form,
				'students':students,
				'teams':teams
			}
	return render(request, "courses/team_swap.html", context)

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

def invite_students(request, data, course_id, course_name):
	emails = data['emails']
	if emails is None or len(emails) == 0:
		return
	emails = emails.split(",")
	i = 0
	while i < len(emails):
		emails[i] = emails[i].strip()
		# prevent duplicate invitations
		if Invitation.objects.filter(student=emails[i], course_id=course_id).count() == 0 and Registration.objects.filter(student=emails[i], course_id=course_id).count() == 0:
			Invitation.objects.create(student=emails[i], course_id=course_id, name=course_name)
		else:
			emails.pop(i)
			i -= 1
		i += 1
	send_email(request, emails, data['code'], data['name'])

# def accept_invite(request, student, course_id):
# 	Invitation.objects.get(student=student, course_id=course_id).delete()
# 	Registration.objects.create(student=student,course_id=course_id,team_id=0)
# 	data = {
# 		"course_list": get_user_registrations(request),
# 		"invitations": get_user_invitations(request)
# 	}
# 	return render(request, 'users/home.html', data)

def handle_invite(request):
	if 'accept' in request.POST:
		return accept_invite(request)
	else:
		return decline_invite(request)

def accept_invite(request):
	student=request.user.email
	course_id = request.POST['accept']
	invite = Invitation.objects.get(student=student, course_id=course_id)
	default_team_id = Team.objects.get(course_id=course_id,team_num=0).team_id
	Registration.objects.create(student=invite.student,course_id=invite.course_id,name=invite.name,team_id=default_team_id)
	invite.delete()
	data = {
		"course_list": get_user_registrations(request),
		"invitations": get_user_invitations(request)
	}
	return render(request, 'users/home.html', data)

def decline_invite(request):
	student=request.user.email
	course_id = request.POST['decline']
	invite = Invitation.objects.get(student=student, course_id=course_id)
	invite.delete()
	data = {
		"course_list": get_user_registrations(request),
		"invitations": get_user_invitations(request)
	}
	return render(request, 'users/home.html', data)

def switch_team(request, student, course_id, team_id):
	reg = Registration.objects.get(student=student,course_id=course_id)
	reg.team_id = team_id
	reg.save()

