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

    def get_context_data(self, *args, **kwargs):
        self.send_message(self.request)
        return super(MessageMixin, self).get_context_data(*args, **kwargs)
