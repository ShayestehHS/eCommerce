from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from address.forms import AddressCreateForm, AddressUpdateForm
from address.models import Address
from carts.utils import get_cart, get_cart_from_session
from eCommerce.mixins import NextUrlMixin
from eCommerce.utils import get_next_url, required_ajax
from orders.models import Order

User = get_user_model()
LIMIT_ADDRESS_TO_USER = getattr(settings, 'LIMIT_ADDRESS_TO_USER', 6)


def get_address_type(address):
    if address.address_type:
        return address.address_type

    addr_type = address.request.GET.get('type')  # querystring is used in checkout page

    if addr_type == 'shipping' or addr_type == 'billing':
        return addr_type
    elif address.order and address.order.address_billing_id:
        return 'shipping'
    elif address.order and address.order.address_shipping_id:
        return 'billing'
    return None


@login_required
@get_cart
@get_next_url
def address_use(request, cart, next_url):
    if not request.is_ajax() and request.method != "POST":
        return HttpResponseBadRequest

    address_id_post = request.POST['address_id']
    address_type = request.POST['address_type']  # billing || shipping
    order = Order.objects.get(user_id=request.user.id, cart=cart)
    address = Address.objects \
        .filter(id=address_id_post, address_type=address_type) \
        .first()

    setattr(order, f'address_{address_type}_id', address.id)
    order.save(update_fields=[f'address_{address_type}_id'])

    messages.success(request, f'Your {address_type} address is changed successfully.')
    path = next_url or reverse('orders:detail', kwargs={'pk': order.pk})
    return redirect(path)


@login_required
@required_ajax
def ajax_list_address(request):
    address_type = request.GET['address_type']
    addresses = Address.objects.filter(user=request.user, address_type=address_type)
    context = {
        'addresses': addresses,
        'address_type': address_type,
    }
    return render(request, 'address/list.html', context)


class AddressListView(LoginRequiredMixin, ListView):
    model = Address
    template_name = 'address/update_address.html'
    context_object_name = 'addresses'

    def get_context_data(self, *args, **kwargs):
        context = super(AddressListView, self).get_context_data(*args, **kwargs)
        context['form'] = AddressUpdateForm()
        context['addresses'] = Address.objects \
            .filter(user=self.request.user) \
            .only('id', 'address_type', 'address_1', 'city')
        return context

    def get_queryset(self):
        request = self.request
        # ToDo: user=request.user => Every user only can see addresses of himself
        address = self.model.objects.filter(user=request.user)
        return address


class AddressCreateView(LoginRequiredMixin, NextUrlMixin, CreateView):
    form_class = AddressCreateForm
    success_url = reverse_lazy('carts:checkout')
    template_name = 'address/set_address.html'

    def __init__(self):
        super(AddressCreateView, self).__init__()
        self.cart = None
        self.order = None
        self.address_type = None

    def get_initial(self):
        initial = super(AddressCreateView, self).get_initial()
        initial['address_type'] = get_address_type(self)

        return initial

    def get_context_data(self, **kwargs):
        context = super(AddressCreateView, self).get_context_data(**kwargs)
        extra_context = {
            'order': self.order,
            'form': kwargs.get('form') or AddressCreateForm(self.request.POST or None),
            'address_type': kwargs.get('address_type') or get_address_type(self),
        }
        context.update(extra_context)
        return context

    def get(self, request, *args, **kwargs):
        self.cart = get_cart_from_session(request)
        if self.cart.products.count() == 0:
            messages.error(request, 'Your cart is empty')
            return redirect('carts:home')

        self.order, created = Order.objects.get_or_create(cart=self.cart, user=request.user)
        self.address_type = get_address_type(self)

        return super(AddressCreateView, self).get(request, *args, **kwargs)

    def form_invalid(self, form):
        request = self.request
        address_type = form.cleaned_data.get('address_type')
        context = self.get_context_data(form=form, address_type=address_type)

        messages.error(request, 'Your form is not valid.')
        return self.render_to_response(context)

    def form_valid(self, form):
        request = self.request
        if Address.objects.filter(user_id=request.user.id).count() >= LIMIT_ADDRESS_TO_USER:
            msg = f'You already have maximal amount of address ({LIMIT_ADDRESS_TO_USER})'
            messages.error(request, msg)
            form.add_error('user', msg)
            return self.form_invalid(form)

        form.instance.user = request.user
        messages.success(request, f'Your address is saved successfully')
        return super(AddressCreateView, self).form_valid(form)


class AddressUpdateView(UpdateView):
    model = Address
    form_class = AddressUpdateForm
    template_name = 'carts/snippets/address_form.html'
    success_url = reverse_lazy('address:list')

    def get_context_data(self, **kwargs):
        context = super(AddressUpdateView, self).get_context_data(**kwargs)
        context['address_id'] = self.object.id
        return context

    def get_object(self, queryset=None):
        obj = super(AddressUpdateView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404('Address not found')
        return obj

    def get_success_url(self):
        messages.success(self.request, 'Your address is updated successfully')
        return super(AddressUpdateView, self).get_success_url()
