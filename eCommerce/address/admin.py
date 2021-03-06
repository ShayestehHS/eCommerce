from django.contrib import admin

from address.models import Address


@admin.register(Address)
class AddressAdminModel(admin.ModelAdmin):
    def get_user_str(self, obj):
        return obj.user

    readonly_fields = ('id',)
    list_display = ('__str__', 'address_type', 'country', 'get_user_str')
    get_user_str.short_description = 'User'
