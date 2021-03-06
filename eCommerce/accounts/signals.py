from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def user_post_save(instance, created, *args, **kwargs):
    if created:
        instance.send_activation_email()
