from django.shortcuts import render

# Create your views here.
def student_view(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username = username, password = password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return redirect('login')
			# redirect to homepage
		else:
			return redirect('error')
			# account is not valid display
	else:
		return redirect('error') 

def admin_view(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username = username, password = password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return redirect('login')
			# redirect to homepage
		else:
			return redirect('error')
			# account is not valid display
	else:
		return redirect('error')
		# login error