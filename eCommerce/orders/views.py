from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from orders.models import Order


class OrderAccountList(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 5
    template_name = 'orders/list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).not_created()


# ToDo: Create PDF file for this data
class OrderAccountDetail(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/detail.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        qs = self.model.objects \
            .filter(user=self.request.user, pk__iexact=pk) \
            .select_related('address_shipping', 'address_billing', 'cart') \
            .first()

        return qs
