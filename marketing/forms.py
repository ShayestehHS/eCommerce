from django import forms

from marketing.models import MarketingPreference


class SubscriptionForm(forms.ModelForm):
    is_subscribed = forms.BooleanField(label="Do you want to get email from us or not?", required=False)

    class Meta:
        model = MarketingPreference
        fields = ['is_subscribed']
