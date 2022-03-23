from django.shortcuts import render, redirect
from .models import Course, Team, StudentTeam
from .forms import CourseForm
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
	return render(request, "courses/course_create.html", {})