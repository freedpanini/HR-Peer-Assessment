from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
	name 		= forms.CharField(widget=forms.TextInput(attrs={"id":"inputCourseName"}))
	semester 	= forms.CharField(widget=forms.TextInput(attrs = {"id":"inputSemester"}))
	year 		= forms.DecimalField(widget=forms.TextInput(attrs = {"id":"inputSemester"}))
	code 		= forms.CharField(widget=forms.TextInput(attrs={"id":"inputCode"}))
	num_teams 	= forms.DecimalField(widget=forms.TextInput(attrs={"id":"inputNumTeams"}))
	class Meta:
		model = Course
		fields = [
			'name',
			'semester',
			'year',
			'code',
			'num_teams'
		]