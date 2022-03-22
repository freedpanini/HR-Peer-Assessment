from django.shortcuts import render

# Create your views here.
def course_creation_view(request):


	return render(request, "users/course_create.html",{})