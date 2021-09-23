from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from orders.models import Order
from orders.forms import AddressForm
from carts.utils import get_cart
from carts.models import Cart
from eCommerce.utils import is_valid_url
from products.models import Product


@get_cart
def cart_home(request, cart):
    products = cart.products.values('id', 'name', 'price')
    total = Cart.objects.filter(id=cart.id).values_list('total', flat=True)

    context = {
        'cart': cart,
        'total': total.first(),
        'products': products,
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

    bill_sipp_type = request.POST['address_type']  # shipping || billing
    address = form.save(commit=False)
    address.user = request.user
    address.cart = cart
    address.address_type = bill_sipp_type
    address.save()

    order, is_new = Order.objects.get_or_create(cart=cart, user=request.user)
    setattr(order, f'address_{bill_sipp_type}', address)
    order.save(update_fields=[f'address_{bill_sipp_type}'])

    messages.success(request, 'Your address is save successfully')
    if not is_valid_url(request, next_page):
        return redirect('carts:checkout')

    return redirect(next_page)


@get_cart
def finalization(request, cart):
    order = Order.objects.get(cart=cart)

    if not order.check_done():  # address_shipping and address_billing is exists
        messages.error(request, 'You have to fill both of'
                                ' billing and shipping addresses.')
        return redirect('carts:home')

    is_deactivated = order.deactivate_cart(request, checked=True)
    if not is_deactivated:
        messages.error(request, 'Something bad is happening,'
                                'Please contact to us')
        return redirect('carts:home')

    return render(request, 'carts/finalization.html')
