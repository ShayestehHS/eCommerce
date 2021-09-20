from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from billing.models import BillingProfile
from carts.utils import get_cart
from carts.models import Cart
from orders.models import Order
from products.models import Product


def update_cart_items_session(req, cart):
    req.session['cart_items'] = cart.products.count()


@get_cart
def cart_home(request, cart):
    products = cart.products.values('id', 'name', 'price')

    context = {
        'cart': cart,
        'products': products
    }
    return render(request, 'carts/cart_home.html', context)


@get_cart
@login_required
def checkout(request, cart):
    if cart.products.count() is 0:
        messages.error(request, 'Your cart is empty')
        return redirect('carts:home')

    billing_profile = BillingProfile.objects.get(user=request.user)
    billing_profile.calculate_total(request.user)

    context = {
        'cart': cart,
        'billing_profile': billing_profile,
    }
    return render(request, 'carts/checkout.html', context)


@get_cart
def remove_product(request, cart):
    product_id = request.POST.get('product_id')

    Cart.objects.remove_product(cart, product_id)
    update_cart_items_session(request, cart)

    # ToDo: request should be AJAX
    product = Product.objects.get(id=product_id)
    return redirect(product.get_absolute_url())


@get_cart
def add_product(request, cart):
    product_id = request.POST.get('product_id')

    Cart.objects.add_product(cart, product_id)
    update_cart_items_session(request, cart)

    # ToDo: request should be AJAX
    product = Product.objects.get(id=product_id)
    return redirect(product.get_absolute_url())
