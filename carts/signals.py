from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver

from decimal import Decimal

from carts.models import Cart

Tax = 0.08


@receiver(m2m_changed, sender=Cart.products.through)
def m2m_changed_cart_receiver(instance, action, *args, **kwargs):
    if 'post_' in action:  # post_save || post_remove || post_clear
        shipping_total = 0
        for product in instance.products.all():
            shipping_total += product.price

        instance.shipping_total = shipping_total
        instance.save(update_fields=['shipping_total'])
        try:
            instance.billing_profile.calculate_total(instance)
        except instance._meta.model.billing_profile.RelatedObjectDoesNotExist:
            pass



@receiver(pre_save, sender=Cart)
def cart_pre_save(sender, instance, **kwargs):
    if instance.subtotal is not 0:
        instance.total = Decimal(instance.subtotal) * Decimal(1 + Tax)
