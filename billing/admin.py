from django.contrib import admin
from billing.models import BillingProfile,Address


@admin.register(BillingProfile)
class BillingProfileAdminModel(admin.ModelAdmin):
    readonly_fields = ('id',)

@admin.register(Address)
class BillingProfileAdminModel(admin.ModelAdmin):
    readonly_fields = ('id',)
