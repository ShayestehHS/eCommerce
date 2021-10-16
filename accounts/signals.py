from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from carts.models import Cart

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def user_post_save(instance, created, *args, **kwargs):
    if created:
        Cart.objects.create(user=instance)
