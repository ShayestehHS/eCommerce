from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from marketing.models import MarketingPreference
from marketing.utils import Mailchimp

USER = settings.AUTH_USER_MODEL


@receiver(pre_save, sender=MarketingPreference)
def check_subscribe_and_mailchimp(sender, instance, *args, **kwargs):
    if instance.is_mailchimp_subscribed != instance.is_subscribed:
        set_to_subscribed = instance.is_subscribed
        mailchimp = Mailchimp()

        status = "subscribed" if set_to_subscribed else "unsubscribed"
        is_successfully = mailchimp.change_status(email=instance.user.email, status=status)
        if is_successfully:
            instance.is_mailchimp_subscribed = True if status == "subscribed" else False


@receiver(post_save, sender=MarketingPreference)
def subscribe_user_on_create(sender, instance, created, *args, **kwargs):
    if created:
        is_subscribed = Mailchimp().subscribe(email=instance.user.email)
        if is_subscribed:
            instance.is_subscribed = True
            instance.is_mailchimp_subscribed = True
            instance.save(update_fields=['is_subscribed', 'is_mailchimp_subscribed'])


@receiver(post_save, sender=USER)
def create_marketing_pref_for_user(sender, instance, created, *args, **kwargs):
    if created and not MarketingPreference.objects.filter(user__id=instance.id).exists():
        MarketingPreference.objects.create(user=instance)
    ## Low performance:
    # if created:
    #   MarketingPreference.objects.get_or_create(user=instance)
