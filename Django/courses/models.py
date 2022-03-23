from django.db import models

# Create your models here.
class Course(models.Model):
	SEMESTERS = (
        ('FALL', 'Fall'),
        ('SPRING', 'Spring'),
        ('SUMMER', 'Summer'),
        ('WINTER', 'Winter')
    )
	name 		= models.CharField(max_length=120, blank=False)
	semester 	= models.CharField(max_length=10, choices=SEMESTERS)
	year 		= models.DecimalField(max_digits=5,decimal_places=0, blank=False)
	code 		= models.CharField(max_length=30, blank=False)
	course_id 	= models.AutoField(primary_key=True)

class Team(models.Model):
	STUDENT_LIST = (
    	('email', 'Email'),
    	('chat', 'Chat'),
    	('call', 'Call'),
	)
	team_name	= models.CharField(max_length=120)
	student_list= models.CharField(max_length=120, choices=STUDENT_LIST, default='')
	team_id 	= models.AutoField(primary_key=True)

# Database table to map student to teams/courses
class StudentTeam(models.Model):
	# Holds username
	student 	= models.CharField(max_length=120,blank=False)
	team_id 	= models.DecimalField(max_digits=20,decimal_places=0, blank=False)

