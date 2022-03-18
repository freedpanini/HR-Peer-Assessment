from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

OCCUPATION_CHOICES =(
    ("STUDENT",'Student'),
    ("PROFESSOR",'Professor'),
)

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField()
    occupation = forms.ChoiceField(choices= OCCUPATION_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2','occupation']