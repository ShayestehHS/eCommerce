from carts.models import Cart


def validate_cart_id(cart_id, req):
    if not isinstance(cart_id, int):
        try:
            cart_id = int(cart_id)
        except ValueError:  # cart_id is something like 'abc'
            del req.session['cart_id']
            req.session.modified = True
            cart_id = 0
        except TypeError:  # cart_id is None
            cart_id = 0

    return cart_id


def get_cart_from_session(req):
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
