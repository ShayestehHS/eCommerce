from django.contrib import admin
from billing.models import BillingProfile


@admin.register(BillingProfile)
class BillingProfileAdminModel(admin.ModelAdmin):
    readonly_fields = ('id',)
