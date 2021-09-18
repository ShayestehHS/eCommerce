from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver

from carts.models import Cart
from orders.models import Order


@receiver(m2m_changed, sender=Cart.products.through)
def m2m_changed_cart_receiver(sender, instance, action, **kwargs):
    if 'post_' in action:  # post_save post_remove post_clear
        subtotal = 0
        for product in instance.products.all():
            subtotal += product.price

        instance.subtotal = subtotal
        instance.total = subtotal  # *1.08
        instance.save(update_fields=['subtotal', 'total'])


@receiver(pre_save, sender=Cart)
def cart_pre_save(sender, instance, **kwargs):
    instance.total = instance.subtotal + 10 if instance.subtotal != 0 else 0


@receiver(post_save, sender=Cart)
def cart_post_save(sender, instance, created, **kwargs):
    print(created)
    if created:
        Order.objects.create(cart=instance)