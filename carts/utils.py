from django.shortcuts import redirect

from functools import wraps

from carts.models import Cart


def get_cart_id(request, cart_id=None):
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


def get_cart_from_session(request):
    cart_id = get_cart_id(request=request)
    cart_obj, is_new = Cart.objects.get_or_new(request=request, id=cart_id)

    if cart_obj.user_id is None:
        if request.user.is_authenticated:
            cart_obj.user_id = request.user.id
            cart_obj.save()

    return cart_obj


def get_cart(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        cart_id = get_cart_id(request)

        kwargs['cart'], is_new = Cart.objects.get_or_new(id=cart_id, request=request)
        return view(request, *args, **kwargs)

    return _wrapped_view
