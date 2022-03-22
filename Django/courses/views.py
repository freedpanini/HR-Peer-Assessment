from django.shortcuts import render
from .models import Course, Team, StudentTeam
from .forms import CourseForm
# Create your views here.
def course_creation_view(request):
	form=CourseForm(request.POST or None)
	if form.is_valid():
		form.save()
		form=CourseForm()
	context={

		'form':form
	}

	return render(request, "users/course_create.html",context)