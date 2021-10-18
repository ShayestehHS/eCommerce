from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from eCommerce.mixins import MessageMixin
from marketing.models import MarketingPreference
from marketing.forms import SubscriptionForm


class UpdateSubscription(MessageMixin, UpdateView):
    form_class = SubscriptionForm
    template_name = 'marketing/subscription.html'
    success_url = reverse_lazy('products:list')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('accounts:login')

        return super(UpdateSubscription, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return MarketingPreference.objects.get(user=self.request.user)
        except MarketingPreference.DoesNotExist:
            raise Exception("Ooops?!")

    def form_valid(self, form):
        is_subscribed = form.cleaned_data['is_subscribed']
        if is_subscribed is True:
            self.message = "You subscribed successfully"
        elif is_subscribed is False:
            self.message = "You unsubscribed successfully"

        return super(UpdateSubscription, self).form_valid(form)
