from django.db import models
from django.conf import settings

from products.models import Product

User = settings.AUTH_USER_MODEL


def get_product(product_id):
    """ Get product with validated product_id """
    if product_id is None:
        raise ValueError('Product id is "None"')

    try:
        product_id = int(product_id)
    except ValueError:
        raise ValueError('Product id is not Integer')

    try:
        obj = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise ValueError(f'Product with id {product_id} is not exists')

    return obj


class CartManager(models.Manager):
    def new(self, request, **kwargs):
        user = request.user if request.user.is_authenticated else None
        cart = self.model.objects.create(user=user, **kwargs)

        old_cart_id = request.session.get('cart_id')
        if old_cart_id:
            self.model.objects.filter(id=old_cart_id, user=None).delete()

        update_session(request, cart,is_new=True)
        return cart

    def get_or_new(self, request, **kwargs):
        user = request.user
        try:
            obj, is_new = self.model.objects.get(**kwargs), False
        except self.model.DoesNotExist:
            obj, is_new = self.model.objects.new(user=user, request=request), True

        # Set the user for not_created carts and delete duplicated carts by same user
        if not is_new and obj.user_id is None and request.user.is_authenticated:
            Cart.objects.exclude(id=obj.id).delete()

            obj.user_id = request.user.id
            obj.save(update_fields=['user'])

        return obj, is_new

    @staticmethod
    def remove_product(cart, product_id):
        product_obj = get_product(product_id)
        cart.products.remove(product_obj)

    @staticmethod
    def add_product(cart, product_id):
        product_obj = get_product(product_id)
        cart.products.add(product_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    products = models.ManyToManyField(Product, blank=True)
    shipping_total = models.DecimalField(max_digits=7, decimal_places=2, default=0,
                                         help_text='Maximum subtotal is 99999.99')
    last_update = models.DateTimeField(auto_now=True)
    crated = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = CartManager()

    def __str__(self):
        return f"cart {self.id}"
