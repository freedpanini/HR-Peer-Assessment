from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

def get_week_ahead():
    return datetime.today() + timedelta(days=7)

class PeerAssessment(models.Model):
    title = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    creation_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=get_week_ahead)
    course_id = models.IntegerField()


class Question(models.Model):
    peer_assessment = models.ForeignKey(PeerAssessment, on_delete=models.CASCADE)
    question = models.CharField(max_length=256)

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=256)

class Submission(models.Model):
    peer_assessment = models.ForeignKey(PeerAssessment, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)

class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

class FreeResponse(models.Model):
    peer_assessment = models.ForeignKey(PeerAssessment, on_delete=models.CASCADE, default=None)
    response = models.CharField(max_length=256)

