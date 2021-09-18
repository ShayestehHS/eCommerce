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

    def new(self, user=None):
        user = user if user and user.is_authenticated else None
        cart = self.model.objects.create(user=user)
        return cart

    def get_or_new(self, user=None, **kwargs):
        try:
            obj, is_new = self.model.objects.get(**kwargs), False
        except self.model.DoesNotExist:
            user = user if user.is_authenticated else None
            obj, is_new = self.model.objects.new(user=user), True

        return obj, is_new

    def remove_product(self, cart, product_id):
        product_obj = get_product(product_id)
        cart.products.remove(product_obj)

    def add_product(self, cart, product_id):
        product_obj = get_product(product_id)
        cart.products.add(product_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)
    products = models.ManyToManyField(Product,
                                      blank=True)
    subtotal = models.DecimalField(max_digits=7, decimal_places=2, default=0,
                                   help_text='Maximum subtotal is 99999.99')
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0,
                                help_text='Maximum total is 99999.99')
    last_update = models.DateTimeField(auto_now=True)
    crated = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def save(self, *args, **kwargs):
        super(Cart, self).save(*args, **kwargs)

    def __str__(self):
        return f"cart {self.id}"



