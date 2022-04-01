from django.db import models
from django.contrib.auth.models import User

class PeerAssessment(models.Model):
    title = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

class Question(models.Model):
    peer_assessment = models.ForeignKey(PeerAssessment, on_delete=models.CASCADE)
    question = models.CharField(max_length=256)

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=256)

class Submission(models.Model):
    survey = models.ForeignKey(PeerAssessment, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)


class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
