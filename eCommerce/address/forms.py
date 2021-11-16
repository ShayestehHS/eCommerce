from django import forms

from address.models import Address
from eCommerce.mixins import BootstrapFieldsForm


class AddressCreateForm(BootstrapFieldsForm, forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
        widgets = {
            'address_1': forms.TextInput(attrs={'placeholder': 'Required'}),
            'address_2': forms.TextInput(attrs={'placeholder': 'Not required'})
        }


class AddressUpdateForm(BootstrapFieldsForm, forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user', 'address_type']
        widgets = {
            'address_1': forms.TextInput(attrs={'placeholder': 'Required'}),
            'address_2': forms.TextInput(attrs={'placeholder': 'Not required'})
        }
