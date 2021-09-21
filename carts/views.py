from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from billing.models import BillingProfile
from billing.forms import AddressForm
from carts.utils import get_cart
from carts.models import Cart
from eCommerce.utils import is_valid_url
from products.models import Product


@get_cart
def cart_home(request, cart):
    products = cart.products.values('id', 'name', 'price')
    context = {
        'cart': cart,
        'products': products
    }
    return render(request, 'carts/cart_home.html', context)


@get_cart
def remove_product(request, cart):
    product_id = request.POST.get('product_id')

    Cart.objects.remove_product(cart, product_id)
    request.session['cart_items'] = cart.products.count()

    messages.error(request, 'Removed from your cart.')
    # ToDo: request should be AJAX
    product = Product.objects.get(id=product_id)
    return redirect(product.get_absolute_url())


@get_cart
def add_product(request, cart):
    product_id = request.POST.get('product_id')

    Cart.objects.add_product(cart, product_id)
    request.session['cart_items'] = cart.products.count()

    messages.success(request, 'Added to your cart.')
    # ToDo: request should be AJAX
    product = Product.objects.get(id=product_id)
    return redirect(product.get_absolute_url())


@get_cart
@login_required
def checkout(request, cart):
    if cart.products.count() == 0:
        messages.error(request, 'Your cart is empty')
        return redirect('carts:home')

    billing_profile, in_new = BillingProfile.objects.get_or_create(cart=cart,
                                                                   is_active=True)
    billing_profile.calculate_total(cart)

    context = {
        'cart': cart,
        'billing_profile': billing_profile,
        'address_form': AddressForm(request.POST or None),
    }
    return render(request, 'carts/checkout.html', context)


@get_cart
def address_create(request, cart):
    form = AddressForm(request.POST)
    next_page = request.POST.get('next')
    if not form.is_valid():
        messages.error(request, 'Your form is not valid.')
        return redirect('carts:checkout')

    form = form.save(commit=False)
    form.billing_profile = BillingProfile.objects.get(cart=cart)
    form.save()

    messages.success(request, 'Your address is save successfully')
    if not is_valid_url(request, next_page):
        return redirect('carts:checkout')

    return redirect(next_page)
