from django import forms
from .models import Course, Team

class CourseForm(forms.Form):
	name 		= forms.CharField(required=True)
	semester 	= forms.CharField(required=True)
	year		= forms.DecimalField(required=True)
	code 		= forms.CharField(required=True)
	emails 		= forms.CharField()
	
class TeamForm(forms.ModelForm):
	team_name	= forms.CharField(required=True)
	class Meta:
		model   = Team
		fields	= ['team_name','team_id']

class TeamSwapForm(forms.Form):
	student 	= forms.EmailField(max_length=120,required=True)
	team_id 	= forms.DecimalField(max_digits=20,required=True)

class AddStudentForm(forms.Form):
	emails 		= forms.CharField()