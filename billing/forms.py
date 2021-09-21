from django import forms
from billing.models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model =Address
        exclude = ('billing_profile',)
