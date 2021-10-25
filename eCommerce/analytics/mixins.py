from analytics.signals import object_viewed_signal


class ObjectViewedMixin(object):

    def get_context_data(self, *args, **kwargs):
        context = super(ObjectViewedMixin, self).get_context_data(*args, **kwargs)
        instance = context.get('object')
        if instance:
            request = self.request
            object_viewed_signal.send(sender=instance.__class__, instance=instance, request=request)
        return context

