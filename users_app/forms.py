from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    firstname=forms.CharField()
    lastname=forms.CharField()

    class Meta:
        model=User
        fields=['firstname','lastname','username','email','password1','password2']