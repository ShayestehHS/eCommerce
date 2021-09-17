from django.db import models

from carts.models import Cart

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):
    order_id = models.CharField(max_length=10, editable=False)

    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(max_digits=7, decimal_places=2,
                                         default=0,
                                         help_text='Maximum total is 99999.99')
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0,
                                help_text='Maximum total is 99999.99')
