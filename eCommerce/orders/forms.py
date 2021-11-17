from django import forms
from orders.models import Payments


class ByMeCoffeeForm(forms.ModelForm):
    full_name = forms.CharField(max_length=127)
    email = forms.EmailField()
    amount = forms.IntegerField(min_value=1000)

    class Meta:
        model = Payments
        fields = ['full_name', 'email', 'amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self.fields
        for field in fields:
            fields[field].widget.attrs.update({'class': 'form-control'})
