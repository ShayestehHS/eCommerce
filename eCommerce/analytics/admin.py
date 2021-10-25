from django.contrib import admin

from analytics.models import ObjectViewed, UserSession


@admin.register(ObjectViewed)
class ObjectViewedModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


@admin.register(UserSession)
class UserModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'active')
    list_display = ['__str__', 'active']
    actions = ['end_session_action']

    @admin.action(description="Inactive and end session")
    def end_session_action(self, request, queryset):
        objs = []
        for session in queryset:
            session.end_session(bulk_update=True)
            objs.append(session)
        UserSession.objects.bulk_update(objs, ['active', 'ended'])
