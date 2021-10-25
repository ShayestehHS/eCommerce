from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from billing.models import BillingProfile

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, *args, **kwargs):
    if created:
        BillingProfile.objects.create(user=instance)
