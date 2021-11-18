from django.contrib import admin

from orders.models import Order, Payments, ProductPurchase


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'order_id')
    list_display = ('__str__', 'status', 'total', 'user')


@admin.register(Payments)
class CartModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


@admin.register(ProductPurchase)
class CartModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
