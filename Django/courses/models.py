from django.db import models
from multiselectfield import MultiSelectField

class Course(models.Model):
	SEMESTERS = (
		('FALL', 'Fall'),
		('SPRING', 'Spring'),
		('SUMMER', 'Summer'),
		('WINTER', 'Winter')
	)
	name = models.CharField(max_length=120, blank=False)
	semester 	= models.CharField(max_length=10, choices=SEMESTERS)
	year 		= models.DecimalField(max_digits=5,decimal_places=0, blank=False)
	code 		= models.CharField(max_length=30, blank=False)
	course_id 	= models.AutoField(primary_key=True)
	professor = models.EmailField(max_length=120)

class Team(models.Model):
	STUDENT_LIST = (
		('Hannah', 'Hannah Brooks'),
		('Zach', 'Zach Crews'),
		('Matthew', 'Matthew Scott'),
		('Fred', 'Fred Pan'),
		('Alec', 'Alec Lobanov'),
		('Yufan', 'Yufan Yang')
	)
	team_name	= models.CharField(max_length=120)
	student_list= MultiSelectField(choices=STUDENT_LIST)
	team_id 	= models.AutoField(primary_key=True)
	team_num	= models.DecimalField(max_digits=3,decimal_places=0, blank=False, default=0)
	course_id	= models.DecimalField(max_digits=20,decimal_places=0, blank=False, default=1)
	
# Storing student information:
class Student(models.Model):
	student_name= models.CharField(max_length=120,blank=False)

# Database table to map students that have accepted invite to teams/courses
class Registration(models.Model):
	# Holds username
	student 	= models.EmailField(max_length=120,blank=False)
	team_id 	= models.DecimalField(max_digits=20,decimal_places=0, blank=False)
	course_id	= models.DecimalField(max_digits=20,decimal_places=0, blank=False)
	name = models.CharField(max_length=120)

# Maps invited students to courses
class Invitation(models.Model):
	student 	= models.EmailField(max_length=120,blank=False)
	course_id 	= models.DecimalField(max_digits=20,decimal_places=0, blank=False)
	name = models.CharField(max_length=120)