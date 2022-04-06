from django import forms
from .models import PeerAssessment, Question, Option, FreeResponse


class PeerAssessmentForm(forms.ModelForm):
    class Meta:
        model = PeerAssessment
        fields = ["title"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question"]

class FreeResponse(forms.ModelForm):
    class Meta:
        model = FreeResponse
        fields = ["response"]

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["option_text"]

