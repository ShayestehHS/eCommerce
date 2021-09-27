from django.contrib import admin
from django.contrib.auth.models import Group

from accounts.models import User, ContactEmail

admin.site.unregister(Group)


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

@admin.register(ContactEmail)
class ContactEmailModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)