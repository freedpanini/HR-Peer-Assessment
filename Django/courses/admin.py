from django.contrib import admin

# Register your models here.
from .models import Course, Team

admin.site.register(Course)
admin.site.register(Team)