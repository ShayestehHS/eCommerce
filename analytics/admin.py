from django.contrib import admin

from analytics.models import ObjectViewed


@admin.register(ObjectViewed)
class ObjectViewedModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
