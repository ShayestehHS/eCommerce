import json
import requests
from django.contrib import messages

from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse

from functools import wraps

from carts.models import Cart
from eCommerce.utils import update_session
from orders.models import Order, ProductPurchase


def get_cart_id_from_session(request, cart_id=None):
    """
        return:
            if valid => cart_id
            if not valid => 0
    """
    cart_id = cart_id or request.session.get('cart_id', 0)
    if not isinstance(cart_id, int):
        try:
            cart_id = int(cart_id)
        except ValueError:  # cart_id is something like 'abc'
            cart_id = 0
            del request.session['cart_id']
            request.session.modified = True

    return cart_id


def get_cart_from_session(request, allow_none=False):
    user = request.user if request.user.is_authenticated else None
    if user:
        try:
            user_cart = Cart.objects.get(user=user, is_active=True)
            update_session(request, user_cart)
            return user_cart
        except Cart.DoesNotExist:
            if allow_none:
                return None

    cart_id = get_cart_id_from_session(request=request)
    cart_obj, is_new = Cart.objects.get_or_new(request=request, pro_id=cart_id)

    return cart_obj


def get_cart(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        kwargs['cart'] = get_cart_from_session(request)

        return view(request, *args, **kwargs)

    return _wrapped_view


def send_request_to_zp(request, amount, email, mobile=None, description=settings.DEFAULT_ZP_DESCRIPTION):
    req_data = {
        "merchant_id": settings.MERCHANT,
        "amount": amount,  # Rial / Required
        "callback_url": request.build_absolute_uri(reverse('carts:zp_verify')),
        "description": description,
        "metadata": {"email": email}
    }
    if mobile:
        req_data['metadata']['mobile'] = mobile

    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=settings.ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)

    try:
        authority = req.json()['data']['authority']
    except TypeError:
        print("-- WE HAVE PROBLEM IN AUTHORITY IN (send_request_to_zp) --")
        print(f"-- (req) IS: {req} --")
        print(f"-- (req.json) IS: {req.json()} --")
        print(f"-- (req.json()['data']) IS: {req.json()['data']} --")
        return HttpResponse(status=500)

    if len(req.json()['errors']) != 0:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")

    return redirect(settings.ZP_API_START_PAY.format(authority=authority))


def done(request):
    cart = get_cart_from_session(request)
    order = Order.objects.get(cart=cart)

    is_deactivated = order.deactivate_cart(request, checked=True)

    if not is_deactivated:
        # ToDo: Send email to admin
        pass

    bulk_list = []
    for pr in cart.products.all():
        bulk_list.append(ProductPurchase(order=order, product=pr))
    ProductPurchase.objects.bulk_create(bulk_list)

    messages.success(request, 'Please wait for the doorbell to ring😎')
    return
