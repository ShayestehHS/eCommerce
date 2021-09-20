from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from orders.utils import unique_order_id_generator


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    if created:
        instance.order_id = unique_order_id_generator(instance, 10)
        instance.save(update_fields=['order_id'])
