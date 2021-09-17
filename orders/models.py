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
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(max_digits=7, decimal_places=2,
                                         default=0,
                                         help_text='Maximum total is 99999.99')
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0,
                                help_text='Maximum total is 99999.99')

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = unique_order_id_generator(self, 10)
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.order_id
