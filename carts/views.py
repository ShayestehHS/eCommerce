from django.shortcuts import render, redirect
from django.contrib import messages

from carts.models import Cart


def validate_cart_id(cart_id, req):
    if cart_id is None or not isinstance(cart_id, int):
        try:
            cart_id = int(cart_id)
        except ValueError:  # cart_id is something like 'abc'
            del req.session['cart_id']
            req.session.modified = True
            cart_id = 0
        except TypeError:  # cart_id is None
            cart_id = 0

    return cart_id


def cart_home(request):
    cart_id = request.session.get('cart_id')
    cart_id = validate_cart_id(cart_id, request)

    cart_obj, is_new = Cart.objects.get_or_new(user=request.user, id=cart_id)
    if is_new:
        request.session['cart_id'] = cart_obj.id

    elif cart_obj.user is None and request.user.is_authenticated:
        cart_obj.user = request.user
        cart_obj.save()

    return render(request, 'carts/home_cart.html')
