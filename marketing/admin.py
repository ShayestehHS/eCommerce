from django.contrib import admin

from marketing.models import MarketingPreference


@admin.register(MarketingPreference)
class MarketingPreferenceModelAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'is_mailchimp_subscribed', 'timestamp', 'updated']
    list_display = ['user', 'is_subscribed']
    list_filter = ['is_subscribed']
    list_per_page = 10  # ToDo: Set this field for all ModelAdmins
