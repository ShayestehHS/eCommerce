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
            order = Order.objects.get(user_id=instance.user_id)
            instance.set_cart_to_order(order)
        except:
            pass


