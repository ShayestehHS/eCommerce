from django.conf import settings
from django.db import models

USER = settings.AUTH_USER_MODEL


class MarketingPreference(models.Model):
    user = models.OneToOneField(USER, on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=True)
    is_mailchimp_subscribed = models.BooleanField(null=True, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)
