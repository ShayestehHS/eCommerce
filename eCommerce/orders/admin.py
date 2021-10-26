from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'order_id')
    list_display = ('__str__', 'status', 'total', 'user')