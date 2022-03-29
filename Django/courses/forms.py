from django import forms
from .models import Course, Team

class CourseForm(forms.Form):
	name 		= forms.CharField(required=True)
	semester 	= forms.CharField(required=True)
	year		= forms.DecimalField(required=True)
	code 		= forms.CharField(required=True)
	emails 		= forms.CharField()
	
class TeamForm(forms.ModelForm):
	STUDENT_LIST = (
    	('Hannah', 'Hannah Brooks'),
    	('Zach', 'Zach Crews'),
    	('Matthew', 'Matthew Scott'),
    	('Fred', 'Fred Pan'),
    	('Alec', 'Alec Lobanov'),
    	('Yufan', 'Yufan Yang')
	)
	student_list = forms.MultipleChoiceField(
        choices=STUDENT_LIST, 
        widget=forms.CheckboxSelectMultiple())
	team_name	= forms.CharField(required=True)
	class Meta:
		model   = Team
		fields	= ['team_name','student_list','team_id']

