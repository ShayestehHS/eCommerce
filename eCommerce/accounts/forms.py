from django import forms
from django.contrib.auth import get_user_model

from accounts.models import ContactEmail

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': "Should be unique"}),
            'full_name': forms.EmailInput(attrs={'placeholder': "We will call you by this name"}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        # user.is_active = False ToDo: Send verification email to user
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self.fields
        for field in fields:
            fields[field].widget.attrs.update({'class': 'form-control'})


class ConfirmForm(forms.Form):
    confirm_code = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self.fields
        for field in fields:
            fields[field].widget.attrs.update({'class': 'form-control'})


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=127)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is None:
            raise forms.ValidationError('Email field is required')

        user_exists = User.objects.filter(email=email).exists()
        if not user_exists:
            raise forms.ValidationError('Any user with this email is not exists.')

        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self.fields
        for field in fields:
            fields[field].widget.attrs.update({'class': 'form-control'})


class ContactEmailForm(forms.ModelForm):
    class Meta:
        model = ContactEmail
        fields = ("email", "full_name", 'message')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self.fields
        for field in fields:
            fields[field].widget.attrs.update({'class': 'form-control'})
