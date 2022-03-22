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
	semester 	= models.CharField(max_length=1, choices=SEMESTERS)
	year 		= models.DecimalField(decimal_places=0, blank=False)
	code 		= models.CharField(max_length=30, blank=False)
	course_id 	= models.AutoField()

class Team(models.Model):
	name 		= models.CharField(max_length=120, blank=False)
	course 		= models.CharField()
	team_id 	= models.AutoField()

# Database table to map student to teams/courses
class StudentTeam(models.Model):
	# Holds username
	student 	= models.CharField(blank=False)
	team_id 	= models.DecimalField(decimal_places=0, blank=False)

