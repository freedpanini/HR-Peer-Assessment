from django.contrib import admin

# Register your models here.
from .models import Course, Team, Invitation, Registration

admin.site.register(Course)
admin.site.register(Team)
admin.site.register(Invitation)
admin.site.register(Registration)