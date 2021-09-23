from django.db import models
from django.conf import settings

from carts.models import Cart
from eCommerce.utils import update_session

User = settings.AUTH_USER_MODEL

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('shipped', 'Shipped'),
    ('paid', 'Paid'),
    ('refunded', 'Refunded'),
)

TYPE_CHOICES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True)
    address_type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    address_1 = models.CharField(max_length=127)
    address_2 = models.CharField(max_length=127, blank=True, null=True)
    country = models.CharField(max_length=63)
    city = models.CharField(max_length=63)
    state = models.CharField(max_length=63)
    postal_code = models.PositiveIntegerField()
    phone_number = models.PositiveIntegerField()

    def __str__(self):
        return self.address_1[0:20]


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                null=True,
                                blank=True)  # ToDo: Delete this line
    cart = models.OneToOneField(to=Cart, on_delete=models.CASCADE,
                                related_name='order')
    order_id = models.CharField(max_length=10, editable=False, blank=True)
    address_shipping = models.OneToOneField(Address, on_delete=models.CASCADE,
                                            related_name='address_shipping',
                                            null=True, blank=True)
    address_billing = models.OneToOneField(Address, on_delete=models.CASCADE,
                                           related_name='address_billing',
                                           null=True, blank=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES,
                              max_length=8, default='created',
                              null=True, blank=True)
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0,
                                help_text='Maximum subtotal is 99999.99')

    def check_done(self):
        order = self
        total = self.total
        address_shipping_exists = bool(order.address_shipping_id)
        address_billing_exists = bool(order.address_billing_id)

        if total > 0 and address_shipping_exists and address_billing_exists:
            return True
        return False

    def deactivate_cart(self, request, checked=False):
        done = True if checked else self.check_done()
        if not done:
            return False

        user_id = self.user_id
        cart = self.cart

        cart.is_active = False
        cart.save(update_fields=['is_active'])

        new_cart = Cart.objects.create(user_id=user_id)

        update_session(request, new_cart, is_new=True)

        return True

    def __str__(self):
        return self.order_id
