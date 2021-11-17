import requests
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from carts.utils import get_cart, get_cart_from_session, send_request_to_zp
from carts.models import Cart
from eCommerce.utils import required_ajax
from orders.models import Order, Payments


@login_required
def verify(request):
    if request.GET.get('Status') != 'OK':
        return HttpResponse('Transaction failed or canceled by user')

    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    req_header = {"accept": "application/json", "content-type": "application/json'"}
    payment = Payments.objects.filter(user=request.user).latest()
    req_data = {
        "merchant_id": settings.MERCHANT,
        "amount": payment.amount,
        "authority": t_authority
    }

    req = requests.post(url=settings.ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
    if len(req.json()['errors']) != 0:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']

        payment.status = 'error'
        payment.save(update_fields=['status'])
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")

    t_status = req.json()['data']['code']
    if t_status == 100:
        response = HttpResponse("Transaction success.\nRefID: " + str(req.json()["data"]["ref_id"]))
        payment.status = 'success'

    elif t_status == 101:
        response = HttpResponse("Transaction submitted : " + str(req.json()['data']['message']))
        payment.status = 'submit'

    else:
        response = HttpResponse('Transaction failed.\nStatus: ' + str(req.json()['data']['message']))
        payment.status = 'failed'

    payment.save(update_fields=['status'])
    return response

@get_cart
def cart_home(request, cart):
    user = request.user
    if not user.is_active or not user.is_registered:
        messages.error(request, "You don't have permission to this page.")
        return redirect('home')

    products = cart.products.values('id', 'name', 'price')

    context = {
        'cart': cart,
        'total': cart.total,
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
    order = Order.objects.get(cart=cart, status='shipped')

    if not order.check_done():  # address_shipping and address_billing is exists
        messages.error(request, 'You have to fill both of billing and shipping addresses.')
        return redirect('carts:home')

    order.total = cart.total
    order.save(update_fields=['total'])
    context = {
        'order': order,
        'cart': cart,
    }
    return render(request, 'carts/finalization.html', context)


@login_required
@get_cart
def done(request, cart):
    order = Order.objects.get(cart=cart, status='shipped')

    if not order.check_done():  # address_shipping and address_billing is exists
        messages.error(request,
                       'You have to fill both of billing and shipping addresses.')
        return redirect('carts:home')

    is_deactivated = order.deactivate_cart(request, checked=True)
    if not is_deactivated:
        messages.error(request, 'Something bad is happening, Please contact to us')
        return redirect('carts:home')
    # ToDo: Send email to customer
    messages.success(request, 'Please wait for the doorbell to ring😎')
    return redirect('home')


class CheckoutTemplateView(TemplateView):
    template_name = 'carts/checkout.html'

    def get_context_data(self, **kwargs):
        cart = get_cart_from_session(self.request)
        order, created = Order.objects.get_or_create(user=self.request.user, cart=cart)

        context = super(CheckoutTemplateView, self).get_context_data(**kwargs)
        context['order'] = order
        context['cart'] = cart
        return context
