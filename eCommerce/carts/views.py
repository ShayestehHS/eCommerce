import requests
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

from carts.utils import done, get_cart, get_cart_from_session, send_request_to_zp
from carts.models import Cart
from eCommerce.utils import required_ajax
from orders.models import Order, Payments


@login_required
def verify(request):
    payment = Payments.objects.filter(user=request.user).latest()

    if request.GET.get('Status') != 'OK':
        payment.status = 'failed'
        payment.save(update_fields=['status'])
        messages.error(request, 'Transaction failed')
        return HttpResponse('Transaction failed or canceled by user')

    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    req_header = {"accept": "application/json", "content-type": "application/json"}
    req_data = {
        "merchant_id": settings.MERCHANT,
        "amount": payment.total,
        "authority": t_authority,
    }

    req = requests.post(url=settings.ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)

    if len(req.json()['errors']) != 0:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']

        payment.status = 'error'
        payment.save(update_fields=['status'])
        messages.error(request, 'Transaction was success but an error accrued')
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")

    request_data = req.json()['data']  # https://docs.zarinpal.com/paymentGateway/guide/
    t_status = request_data['code']
    if t_status == 100:
        # response = HttpResponse("Transaction success.\nRefID: " + str(request_data["ref_id"]))
        messages.success(request, 'Your transaction was successful.')
        payment.status = 'success'
        payment.ref_id = request_data['ref_id']
        payment.fee = request_data['fee']
        done(request)

    elif t_status == 101:
        # response = HttpResponse("Transaction submitted : " + str(request_data['message']))
        messages.error(request, 'Your transaction was submitted before.')
        payment.status = 'submit'

    else:
        # response = HttpResponse('Transaction failed.\nStatus: ' + str(request_data['message']))
        messages.error(request, 'Transaction failed')
        payment.status = 'failed'

    payment.save()
    return render(request, 'carts/verify.html', context={'payment': payment})


@login_required
def cart_home(request):
    user = request.user
    if not user.is_active or not user.is_registered:
        messages.error(request, "You don't have permission to this page.")
        return redirect('home')

    cart = get_cart_from_session(request, allow_none=True)
    products = None
    if cart is not None:
        products = cart.products.values('id', 'name', 'price')

    context = {
        'cart': cart,
        'products': products,
    }
    return render(request, 'carts/cart_home.html', context)


@required_ajax
@get_cart
def add_rmv_product(request, cart):
    product_id = request.POST.get('product_id')
    product, added = Cart.objects.add_or_remove_product(cart, product_id)
    cart_items = cart.products.count()
    request.session['cart_items'] = cart_items

    msg = 'Added to your cart.' if added else 'Removed from your cart.'
    messages.success(request, msg)
    return JsonResponse({
        'added': added,
        'removed': not added,
        'cart_items': cart_items
    })


@login_required
@required_ajax
@get_cart
def remove(request, cart):
    product_id = request.POST['product_id']
    product = cart.products.get(id=product_id)
    cart.products.remove(product)
    request.session['cart_items'] = cart.products.count()
    data = {'total': cart.total, 'subtotal': cart.subtotal}
    return JsonResponse(data)


@login_required
@get_cart
def finalization(request, cart):
    order = Order.objects.filter(cart=cart) \
        .select_related('cart') \
        .first()  # We need cart in check_done() => self.cart

    if not order.check_done():  # address_shipping and address_billing is exists
        messages.error(request, 'You have to fill both of billing and shipping addresses.')
        return redirect('carts:home')

    context = {
        'order': order,
        'cart': cart,
    }
    return render(request, 'carts/finalization.html', context)


@login_required
@get_cart
def send_to_payment(request, cart):
    if request.method == "GET":
        user = request.user
        order = Order.objects.filter(cart=cart, user=user).only('total').first()
        if not order.check_done():
            messages.error(request, 'You are not done,yet.')
            return redirect('home')

        order.status = 'shipped'
        order.save(update_fields=['status'])
        Payments.objects.get_or_create(full_name=user.full_name, order=order,
                                       user=user, amount=order.total)
        return send_request_to_zp(request, int(order.total) * 1000, user.email)


class CheckoutTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'carts/checkout.html'

    def __init__(self):
        super(CheckoutTemplateView, self).__init__()
        self.cart = None

    def get_context_data(self, **kwargs):
        cart = self.cart or get_cart_from_session(self.request)
        order, created = Order.objects.get_or_create(user=self.request.user, cart=cart)

        context = super(CheckoutTemplateView, self).get_context_data(**kwargs)
        context['order'] = order
        context['cart'] = cart
        return context

    def get(self, request, *args, **kwargs):
        self.cart = get_cart_from_session(request)

        order, created = Order.objects.get_or_create(user=request.user, cart=self.cart)

        if not self.cart.order.check_done():
            addr_type = 'shipping' if not self.cart.is_all_digital and order.address_billing_id else 'billing'
            return redirect(reverse('address:set_address') + f'?type={addr_type}&next={request.META.get("HTTP_REFERER")}')
        return super(CheckoutTemplateView, self).get(request, *args, **kwargs)
