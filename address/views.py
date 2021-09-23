from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from address.models import Address


class AddressListView(LoginRequiredMixin, ListView):
    model = Address
    queryset = Address.objects.filter(user__isnull=False)

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest
