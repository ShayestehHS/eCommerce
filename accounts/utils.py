from carts.models import Cart
from carts.utils import get_cart_id_from_session
from eCommerce.utils import update_session


def set_cart_to_user(request):
    cart_id = get_cart_id_from_session(request)
    if not cart_id:
        # Check into db for cart
        user_cart = Cart.objects.filter(user=request.user, is_active=True)
        if not user_cart.exists():
            user_cart = Cart.objects.new(request=request)

        update_session(request, user_cart)
        return True

    cart = Cart.objects.get(id=cart_id)
    if cart.is_active and cart.user_id == request.user.id:
        return True

    # Delete old_user_carts
    Cart.objects.filter(user_id=request.user.id, is_active=True).delete()

    cart.user_id = request.user.id
    cart.save(update_fields=['user_id'])
    return True
