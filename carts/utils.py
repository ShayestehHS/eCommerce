from functools import wraps

from carts.models import Cart
from eCommerce.utils import update_session


def get_cart_id_from_session(request, cart_id=None):
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
    user = request.user if request.user.is_authenticated else None
    if user:
        user_cart = Cart.objects.filter(user=user, is_active=True)
        if user_cart.exists():
            user_cart = user_cart.first()
            update_session(request, user_cart)
            return user_cart

    cart_id = get_cart_id_from_session(request=request)
    cart_obj, is_new = Cart.objects.get_or_new(request=request, id=cart_id)

    return cart_obj


def get_cart(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        kwargs['cart'] = get_cart_from_session(request)

        return view(request, *args, **kwargs)

    return _wrapped_view
