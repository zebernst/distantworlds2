from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CommanderForm(forms.ModelForm):
    class Meta:
        model = Commander
        # exclude = ['user']
        fields = ('cmdr_name', 'roster_num')


class SignUpForm(UserCreationForm):
    cmdr_name = forms.CharField(max_length=25)
    roster_num = forms.IntegerField(min_value=1, max_value=5000)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'cmdr_name', 'roster_num', 'email')