import requests
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings

from orders.models import Order
from address.forms import AddressForm
from carts.utils import get_cart
from carts.models import Cart, Payments
from eCommerce.utils import is_valid_url, required_ajax


@login_required
def verify(request):
    if request.GET.get('Status') != 'OK':
        return HttpResponse('Transaction failed or canceled by user')

    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    req_header = {"accept": "application/json", "content-type": "application/json'"}
    req_data = {
        "merchant_id": settings.MERCHANT,
        "amount": Payments.objects.filter(user=request.user).latest().only('amount'),
        "authority": t_authority
    }

    req = requests.post(url=settings.ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
    if len(req.json()['errors']) != 0:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")

    t_status = req.json()['data']['code']
    if t_status == 100:
        return HttpResponse("Transaction success.\nRefID: " + str(req.json()["data"]["ref_id"]))

    elif t_status == 101:
        return HttpResponse("Transaction submitted : " + str(req.json()['data']['message']))

    else:
        return HttpResponse('Transaction failed.\nStatus: ' + str(req.json()['data']['message']))


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
def checkout(request, cart):
    if cart.products.count() == 0:
        messages.error(request, 'Your cart is empty')
        return redirect('carts:home')

    order, is_new = Order.objects.get_or_create(cart=cart, user=request.user)
    if order.status == 'created':
        order.status = 'shipped'
        order.save(update_fields=['status'])

    context = {
        'order': order,
        'form': AddressForm(request.POST or None),
    }
    return render(request, 'carts/checkout.html', context)


@login_required
@get_cart
def set_address_to_order(request, cart):
    form = AddressForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Your form is not valid.')
        return redirect('carts:checkout')

    bill_sipp_type = request.POST['address_type']  # shipping || billing
    address = form.save(commit=False)
    address.user = request.user
    address.address_type = bill_sipp_type
    address.save()

    order, is_new = Order.objects.get_or_create(cart=cart, user=request.user)
    setattr(order, f'address_{bill_sipp_type}', address)
    order.save(update_fields=[f'address_{bill_sipp_type}'])

    msg = f'Your {bill_sipp_type} address is saved successfully'
    messages.success(request, msg)

    if order.check_done():
        return redirect('carts:finalization')

    messages.error(request, 'one address is available to fill')
    next_page = request.POST.get('next')
    if not is_valid_url(request, next_page):
        return redirect('carts:checkout')
    return redirect(next_page)


@login_required
@get_cart
def finalization(request, cart):
    order = Order.objects.get(cart=cart, status='shipped')

    if not order.check_done():  # address_shipping and address_billing is exists
        messages.error(request,
                       'You have to fill both of billing and shipping addresses.')
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
