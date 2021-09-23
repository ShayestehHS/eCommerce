from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=127)
    password = forms.CharField(max_length=300, widget=forms.PasswordInput)
