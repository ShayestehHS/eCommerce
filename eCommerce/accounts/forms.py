from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login

from accounts.models import ContactEmail
from accounts.utils import set_cart_to_user
from analytics.signals import user_logged_in_signal
from eCommerce.mixins import BootstrapFieldsForm

User = get_user_model()


class ChangeDetailForm(BootstrapFieldsForm, forms.ModelForm):
    full_name = forms.CharField(max_length=127)

    class Meta:
        model = User
        fields = ['full_name']


class RegisterForm(BootstrapFieldsForm, forms.ModelForm):
    password1 = forms.CharField(max_length=127, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=127, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'full_name']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': "Should be unique"}),
            'full_name': forms.TextInput(attrs={'placeholder': "We will call you by this name"}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.save()
        return user


class ConfirmForm(BootstrapFieldsForm, forms.Form):
    confirm_code = forms.IntegerField()


class LoginForm(BootstrapFieldsForm, forms.Form):
    email = forms.EmailField(max_length=127)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is None:
            user = User.objects.filter(email=email).only('is_active').first()
            if not user.is_active:
                messages.error(request, 'This email is inactive')
                return self.add_error('email', 'This email is inactive')

            elif not user.is_registered:
                messages.error(request, "Please register your email and try again.")
                return self.add_error('email', "Please register your email and try again.")

            else:  # ToDo: Correct way to raise error in clean method
                return self.add_error('password', 'Password is not correct')
        login(request, user)
        set_cart_to_user(request)
        user_logged_in_signal.send(user.__class__, instance=user, request=request)

        return data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is None:
            raise forms.ValidationError('Email field is required')

        user_exists = User.objects.filter(email=email).exists()
        if not user_exists:
            raise forms.ValidationError('Any user with this email is not exists.')

        return email

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)


class ContactEmailForm(BootstrapFieldsForm, forms.ModelForm):
    class Meta:
        model = ContactEmail
        fields = ("email", "full_name", 'message')
