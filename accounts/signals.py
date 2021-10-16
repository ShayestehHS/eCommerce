from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

from analytics.models import UserSession
from analytics.utils import get_client_ip
from carts.models import Cart

User = settings.AUTH_USER_MODEL
user_logged_in_signal = Signal(providing_args=['instance', 'request'])


@receiver(user_logged_in_signal)
def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    UserSession.objects.create(
        user=instance,
        ip_address=get_client_ip(request),
        session_key=request.session.session_key,
    )


@receiver(post_save, sender=User)
def user_post_save(instance, created, *args, **kwargs):
    if created:
        Cart.objects.create(user=instance)
