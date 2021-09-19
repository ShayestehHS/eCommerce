from django.shortcuts import redirect, render

from accounts.forms import LoginForm
from carts.utils import get_cart_from_session, get_cart, get_cart_id
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
def checkout(request, cart):
    order = Order.objects.get(cart=cart)
    form = LoginForm(request.POST or None)
    billing_profile = None

    context = {
        'order': order,
        'cart': cart,
        'login_form': form,
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
