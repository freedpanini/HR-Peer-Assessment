from django import forms
from .models import PeerAssessment, Question, Option


class SurveyForm(forms.ModelForm):
    class Meta:
        model = PeerAssessment
        fields = ["title"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question"]


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["option_text"]

