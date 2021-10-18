from django.contrib import messages


class MessageMixin(object):
    message = ''
    message_level = messages.SUCCESS  # Default tag
    message_delete_other = False

    def send_message(self, request):
        if self.message_delete_other is True:
            """ Delete stored messages """
            storage = messages.get_messages(request)
            storage.used = True

        messages.add_message(request=request, level=self.message_level, message=self.message)

    def dispatch(self, *args, **kwargs):
        response = super(MessageMixin, self).dispatch(*args, **kwargs)
        self.send_message(self.request)
        return response
