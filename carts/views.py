from django.shortcuts import redirect, render
from django.views.generic import ListView, UpdateView

from carts import utils
from carts.models import Cart
from products.models import Product


def update_cart_items_session(req, cart):
    req.session['cart_items'] = cart.products.count()


def cart_home(request):
    cart_obj = utils.get_cart_from_session(request)
    products = cart_obj.products.values('id', 'name', 'price')
    context = {'cart': cart_obj, 'products': products}
    return render(request, 'carts/cart_home.html', context)


def remove_product(request):
    product_id = request.POST.get('product_id')
    cart = utils.get_cart_from_session(request)

    Cart.objects.remove_product(cart, product_id)
    update_cart_items_session(request, cart)

    # ToDo: request should be AJAX
    product = Product.objects.get(id=product_id)
    return redirect(product.get_absolute_url())


def add_product(request):
    product_id = request.POST.get('product_id')
    cart = utils.get_cart_from_session(request)

    Cart.objects.add_product(cart, product_id)
    update_cart_items_session(request, cart)

    # ToDo: request should be AJAX
    product = Product.objects.get(id=product_id)
    return redirect(product.get_absolute_url())
