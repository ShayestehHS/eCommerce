from django.shortcuts import redirect

from functools import wraps

from carts.models import Cart


def validate_cart_id(cart_id, req):
    """
        return:
            if valid => cart_id
            if not valid => 0
    """
    if not isinstance(cart_id, int):
        try:
            cart_id = int(cart_id)
        except ValueError:  # cart_id is something like 'abc'
            cart_id = 0
            del req.session['cart_id']
            req.session.modified = True

    return cart_id


def get_cart_from_session(req, need_order=False):
    cart_id = req.session.get('cart_id', 0)
    cart_id = validate_cart_id(cart_id, req)

    cart_obj, is_new = Cart.objects.get_or_new(user=req.user, id=cart_id)

    if is_new:
        req.session['cart_id'] = cart_obj.id

    elif cart_obj.user_id is None:
        if req.user.is_authenticated:
            cart_obj.user_id = req.user.id
            cart_obj.save()

    return cart_obj


def require_cart_obj(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        cart_id = request.session.get('cart_id', 0)
        cart_id = validate_cart_id(cart_id, request)

        is_exists = Cart.objects.filter(id=cart_id).exists()
        if is_exists:
            return view(request, *args, **kwargs)
        else:
            return redirect('cart:home')

    return _wrapped_view


def get_cart_obj(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        cart_id = request.session.get('cart_id', 0)
        cart_id = validate_cart_id(cart_id, request)
        try:
            cart_obj = Cart.objects.get(id=cart_id)
            kwargs['cart_obj'] = cart_obj
            return view(request, *args, **kwargs)
        except Cart.DoesNotExist:
            return redirect('carts:home')

    return _wrapped_view
