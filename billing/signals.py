from comment.signals import post_save
from django.dispatch import receiver

from billing.models import BillingProfile


@receiver(post_save, sender=BillingProfile)
def cart_post_save(instance, created, *args, **kwargs):
    if created:
        instance.calculate_total(instance.cart)
