from django import forms
from .models import Course

class CourseForm(forms.Form):
	# name 		= forms.CharField(widget=forms.TextInput(attrs={"id":"inputCourseName"}))
	# semester 	= forms.CharField(widget=forms.TextInput(attrs = {"id":"inputSemester"}))
	# year 		= forms.DecimalField(widget=forms.TextInput(attrs = {"id":"inputYear"}))
	# code 		= forms.CharField(widget=forms.TextInput(attrs={"id":"inputCode"}))
	name 		= forms.CharField(required=True)
	semester 	= forms.CharField(required=True)
	year 		= forms.DecimalField(required=True)
	code 		= forms.CharField(required=True)
	# class Meta:
	# 	model = Course
	# 	fields = [
	# 		'name',
	# 		'semester',
	# 		'year',
	# 		'code',
	# 		'num_teams'
	# 	]