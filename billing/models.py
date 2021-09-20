from decimal import Decimal

from django.db import models
from django.conf import settings

from carts.models import Cart

User = settings.AUTH_USER_MODEL


class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    last_update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0,
                                help_text='Maximum total is 99999.99')

    def calculate_total(self, user):
        shipping_total = Cart.objects.filter(
            user=user).values_list('shipping_total', flat=True)[0]
        self.total = Decimal(shipping_total) * Decimal(1.08)
        self.save(update_fields=['total'])

    def __str__(self):
        return str(self.user)
