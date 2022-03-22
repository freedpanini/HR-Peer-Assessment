from django.shortcuts import render

# Create your views here.
def course_creation_view(request):


	return render(request, "create_course.html",{})