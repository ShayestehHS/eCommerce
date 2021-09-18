from django.contrib import admin

from accounts.models import User

@admin.register(User)
class UserAdminModel(admin.ModelAdmin):
    readonly_fields = ('id',)
