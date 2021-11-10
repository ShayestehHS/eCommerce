from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.sessions.models import Session

User = settings.AUTH_USER_MODEL


class ObjectViewedQuerySet(models.query.QuerySet):
    def get_object(self, class_model, paginated, *fields):
        if len(fields) == 0 or paginated <= 0:
            raise ValueError('Error in requirements of function.')
        c_type = ContentType.objects.get_for_model(class_model)
        object_ids = self.filter(content_type=c_type).values_list('object_id', flat=True)[:paginated]
        if object_ids.count() <= 0:
            return [None]

        object_ids_len = len(object_ids)
        matrix_id_object = [[None, None]] * object_ids_len
        for x in range(object_ids_len):
            matrix_id_object[x][0] = object_ids[x]
        objects = class_model.objects.only(*fields).in_bulk(object_ids)
        qs = [objects[id] for id in object_ids]
        return qs


class ObjectViewedManager(models.Manager):

    def get_queryset(self):
        return ObjectViewedQuerySet(self.model, using=self._db)

    def get_object(self, class_model, *fields):
        return self.get_queryset().get_object(class_model, *fields)


class ObjectViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # ip_address = models.GenericIPAddressField()
    ip_address = models.CharField(max_length=127)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ObjectViewedManager()

    def __str__(self):
        return f'{self.content_object} viewed on {self.timestamp}'

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.CharField(max_length=127)
    session_key = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)

    def end_session(self, bulk_update=False):
        session_key = self.session_key
        try:
            Session.objects.get(pk=session_key).delete()
        except Session.DoesNotExist:
            print(f"ERROR: Session DoesNotExist (session key is {session_key})")
            bulk_update = False  # Force to update the instance

        self.ended = True
        self.active = False
        if bulk_update is False:
            self.save(update_fields=['ended', 'active'])

        return self.ended

    def __str__(self):
        return str(self.user)
