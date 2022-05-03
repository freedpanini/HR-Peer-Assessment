from django import forms
from django.contrib.auth.models import User
from .models import FreeResponseAnswer, PeerAssessment, Question, Option, FreeResponse, Submission
from django.forms import HiddenInput

class PeerAssessmentForm(forms.ModelForm):
    class Meta:
        model = PeerAssessment
        fields = ["title", "creation_date", "end_date"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question"]

class FreeResponseForm(forms.ModelForm):
    class Meta:
        model = FreeResponse
        fields = ["response"]

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["option_text", "value"]

class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        options = kwargs.pop("options")
        choices = {(o.pk, o.option_text) for o in options}
        super().__init__(*args, **kwargs)
        option_field = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, required=True)
        self.fields["option"] = option_field

class FreeResponseAnswerForm(forms.ModelForm):
    class Meta:
        model = FreeResponseAnswer
        fields = ["response_answer"]

class BaseAnswerFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["options"] = kwargs["options"][index]
        return kwargs

class SubmissionForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(queryset=User.objects.all())
    class Meta:
        model = Submission
        fields = ['assigned_to']
