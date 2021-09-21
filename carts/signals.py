from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from carts.models import Cart
from orders.models import Order


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


@receiver(post_save, sender=Cart)
def cart_post_save(instance, created, *args, **kwargs):
    if created:
        Order.objects.create(cart=instance)
