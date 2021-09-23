from django.db.models.signals import m2m_changed, post_save
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

        user_id = instance.user_id
        if user_id:
            order, is_new = Order.objects.get_or_create(user_id=user_id, cart=instance)
            instance.set_cart_to_order(order)


@receiver(post_save, sender=Cart)
def cart_post_save(instance, created, *args, **kwargs):
    if created and instance.user_id:
        try:
            order = Order.objects.get(user_id=instance.user_id)
            instance.set_cart_to_order(order)
        except:
            pass


