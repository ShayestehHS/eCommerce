from django.contrib import admin

from carts.models import Cart


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('__str__', 'is_active', 'user', 'last_update')
