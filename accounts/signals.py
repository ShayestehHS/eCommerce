from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from carts.models import Cart
from orders.models import Order
from billing.models import BillingProfile

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        cart = Cart.objects.create(user=instance)
        BillingProfile.objects.create(user=instance)
        Order.objects.create(cart=cart)
