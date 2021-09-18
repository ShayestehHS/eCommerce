from django import forms
from django.conf import settings

User = settings.AUTH_USER_MODEL


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=127)
    password = forms.CharField(max_length=300,widget=forms.PasswordInput)
