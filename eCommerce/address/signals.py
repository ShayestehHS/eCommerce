from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

from address.models import Address
from orders.models import Order

LIMIT_ADDRESS_TO_USER = getattr(settings, 'LIMIT_ADDRESS_TO_USER', 6)


@receiver(post_save, sender=Address)
def address_post_save(sender, instance, created, *args, **kwargs):
    if created:
        if Address.objects.filter(user_id=instance.user.id).count() >= LIMIT_ADDRESS_TO_USER:
            raise ValidationError(f'You already have maximal amount of address ({LIMIT_ADDRESS_TO_USER})')

        order = Order.objects.get(user=instance.user,
                                  cart__user=instance.user, cart__is_active=True)
        address_type = instance.address_type

        setattr(order, f'address_{address_type}', instance)
        order.save(update_fields=[f'address_{address_type}'])
