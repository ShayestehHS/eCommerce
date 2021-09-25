from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render

from orders.models import Order
from address.forms import AddressForm
from carts.utils import get_cart
from carts.models import Cart
from eCommerce.utils import is_valid_url


@get_cart
def cart_home(request, cart):
    products = cart.products.values('id', 'name', 'price')

    context = {
        'cart': cart,
        'total': cart.total,
        'products': products,
    }
    return render(request, 'carts/cart_home.html', context)


@get_cart
def add_rmv_product(request, cart):
    if not request.is_ajax:
        return HttpResponseBadRequest

    product_id = request.POST.get('product_id')
    product, added = Cart.objects.add_or_remove_product(cart, product_id)

    request.session['cart_items'] = cart.products.count()

    msg = 'Added to your cart.' if added else 'Removed from your cart.'
    messages.success(request, msg)
    return JsonResponse({'added': added, 'removed': not added})


@get_cart
@login_required
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


@get_cart
def done(request, cart):
    order = Order.objects.get(cart=cart, status='shipped')

    if not order.check_done():  # address_shipping and address_billing is exists
        messages.error(request, 'You have to fill both of billing and shipping addresses.')
        return redirect('carts:home')

    is_deactivated = order.deactivate_cart(request, checked=True)
    if not is_deactivated:
        messages.error(request, 'Something bad is happening, Please contact to us')
        return redirect('carts:home')

    messages.success(request, 'Please wait for the doorbell to ring😎')
    return redirect('home')
