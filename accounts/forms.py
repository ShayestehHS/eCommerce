from django import forms

from accounts.models import ContactEmail


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=127)
    password = forms.CharField(max_length=300, widget=forms.PasswordInput)


class ContactEmailForm(forms.ModelForm):
    class Meta:
        model = ContactEmail
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self.fields
        for field in fields:
            fields[field].widget.attrs.update({'class': 'form-control'})
