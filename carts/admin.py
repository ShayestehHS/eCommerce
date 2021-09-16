from django.contrib import admin

from carts.models import Cart

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    pass
