from django.db import models
from django.conf import settings

from decimal import Decimal

from carts.models import Cart

User = settings.AUTH_USER_MODEL
TYPE_CHOICES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)


class BillingProfile(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='billing_profile', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0,
                                help_text='Maximum total is 99999.99')

    def calculate_total(self, cart):
        shipping_total = cart.shipping_total
        self.total = Decimal(shipping_total) * Decimal(1.08)
        self.save(update_fields=['total'])

    def deactivate(self):
        user_id = self.cart.user_id
        cart = self.cart
        billing = self

        cart.is_active, billing.is_active = False
        cart.save(update_fields=['is_active'])
        billing.save(update_fields=['is_active'])

        Cart.objects.create(user_id=user_id)
        BillingProfile.objects.create(cart=cart)
        # after that: should call update_session(request) in view

    def __str__(self):
        return str(self.cart.user)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=8, choices=TYPE_CHOICES, default='billing')
    address_1 = models.CharField(max_length=127)
    address_2 = models.CharField(max_length=127, blank=True, null=True)
    country = models.CharField(max_length=63)
    city = models.CharField(max_length=63)
    state = models.CharField(max_length=63)
    postal_code = models.PositiveIntegerField()
    phone_number = models.PositiveIntegerField()
