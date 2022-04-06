from django.contrib import admin
# Register your models here.
from .models import FreeResponse, PeerAssessment, Question, Option, Submission, Answer

admin.site.register(PeerAssessment)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Submission)
admin.site.register(Answer)
admin.site.register(FreeResponse)
