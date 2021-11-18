from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from carts.models import Cart
from orders.models import Order


@receiver(m2m_changed, sender=Cart.products.through)
def m2m_changed_cart_receiver(instance, action, *args, **kwargs):
    if 'post_' in action:  # post_save || post_remove || post_clear
        subtotal = 0
        for product in instance.products.all():
            subtotal += product.price

        instance.subtotal = subtotal
        instance.total = instance.calculate_total(subtotal)
        instance.save(update_fields=['subtotal', 'total'])

        order, created = Order.objects.get_or_create(cart=instance, user=instance.user)
        order.total = instance.total
        order.save(update_fields=['total'])
