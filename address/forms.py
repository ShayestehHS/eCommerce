from django import forms

from address.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('address_type',)
        widgets = {
            'address_1': forms.TextInput(attrs={'placeholder': 'Required'}),
            'address_2': forms.TextInput(attrs={'placeholder': 'Not required'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self.fields
        for field in fields:
            fields[field].widget.attrs.update({'class': 'form-control'})
