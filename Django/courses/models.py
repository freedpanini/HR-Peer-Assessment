from django.db import models

# Create your models here.
class Course(models.Model):
	name = models.CharField(max_length=120, blank=False) 
	semester = models.CharField(max_length=20)
	year = models.DecimalField(decimal_places=0, blank=False)
	code = models.CharField(max_length=30, blank=False)
	num_teams = models.DecimalField(decimal_places=0, blank=False)

class Team(models.Model):
	name = models.CharField(max_length=120, blank=False)
