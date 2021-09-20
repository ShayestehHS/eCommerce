from django.db import models

from carts.models import Cart

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):
    cart = models.OneToOneField(to=Cart, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=10, editable=False, blank=True)
    status = models.CharField(max_length=8, choices=ORDER_STATUS_CHOICES, default='created')

    def __str__(self):
        return self.order_id
