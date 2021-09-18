from django.db import models

from carts.models import Cart
from orders.utils import unique_order_id_generator

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):
    order_id = models.CharField(max_length=10, editable=False, blank=True)
    cart = models.OneToOneField(to=Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(max_digits=7, decimal_places=2,
                                         default=0,
                                         help_text='Maximum total is 99999.99')
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0,
                                help_text='Maximum total is 99999.99')

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        self.total = cart_total + shipping_total
        self.save(update_fields=['total'])

    def __str__(self):
        return self.order_id
