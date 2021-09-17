from django.contrib import admin
from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ['name', 'slug']
    ordering = ['name']
