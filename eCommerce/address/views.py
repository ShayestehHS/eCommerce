from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import ListView

from accounts.utils import CustomLoginRequiredMixin
from address.models import Address
from orders.models import Order

User = get_user_model()


class AddressListView(CustomLoginRequiredMixin, ListView):
    model = Address
    queryset = Address.objects.filter(user__isnull=False)
    http_method_names = ['get']
    template_name = 'address/list.html'
    context_object_name = 'addresses'
    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        context = super(AddressListView, self).get_context_data(*args, **kwargs)
        context['ship_bill'] = self.request.GET['address_type']
        return context

    def get_queryset(self):
        request = self.request
        user = request.user
        address_type = request.GET['address_type']
        return self.queryset.filter(user=user, address_type=address_type)


@login_required
def address_use(request):
    if not request.is_ajax() and request.method != "POST":
        return HttpResponseBadRequest

    address_id_post = request.POST['address_id']
    address_type = request.POST['address_type']  # billing || shipping
    order = Order.objects.get(user_id=request.user.id, status='shipped')
    address_id = Address.objects \
        .filter(id=address_id_post, address_type=address_type) \
        .values_list('id', flat=True) \
        .first()

    setattr(order, f'address_{address_type}_id', address_id)
    order.save(update_fields=[f'address_{address_type}_id'])

    status = 1 if order.check_done() else 0

    return JsonResponse({'status': status})
