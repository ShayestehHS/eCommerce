from django.contrib import admin
from django.contrib.auth.models import Group

from accounts.models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdminModel(admin.ModelAdmin):
    readonly_fields = ('id',)
