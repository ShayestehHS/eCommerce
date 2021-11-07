from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

from analytics.models import ObjectViewed, UserSession
from analytics.utils import get_client_ip

LIMIT_SESSION = getattr(settings, 'FORCE_SESSION', True)
LIMIT_SESSION_COUNT = getattr(settings, 'FORCE_SESSION_COUNT', 1)
object_viewed_signal = Signal(providing_args=['instance', 'request'])
user_logged_in_signal = Signal(providing_args=['instance', 'request'])


@receiver(user_logged_in_signal)
def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    UserSession.objects.create(
        user=instance,
        ip_address=get_client_ip(request),
        session_key=request.session.session_key,
    )


@receiver(object_viewed_signal)
def object_viewed_signal_receiver(sender, instance, request, *args, **kwargs):
    ObjectViewed.objects.create(
        user=request.user,
        content_type=ContentType.objects.get_for_model(sender),
        object_id=instance.id,
        ip_address=get_client_ip(request),
    )


def user_session_post_save(sender, instance, created, *args, **kwargs):
    print(created)
    if created:
        print('user: '+ str(instance.user))
        print('user: '+ str(instance.id))
        old_user_sessions = UserSession.objects.filter(user=instance.user, ended=False, active=True).exclude(id=instance.id)
        print(old_user_sessions.count())
        if old_user_sessions.count() >= LIMIT_SESSION_COUNT:
            objs = []
            for session in old_user_sessions:
                session.end_session(bulk_update=True)
                objs.append(session)
            UserSession.objects.bulk_update(objs, ['ended', 'active'])


@receiver(post_save, sender=UserSession)
def user_session_changed_post_save(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.ended is False and instance.active is not True:
            instance.end_session()

        if instance.ended is True and instance.active is not False:
            instance.end_session()


if LIMIT_SESSION is True:
    post_save.connect(user_session_post_save, sender=UserSession)
