from django.utils.http import is_safe_url
from django.contrib import messages


def is_valid_url(request, url, require_https=False):
    allowed_hosts = request.get_host()
    if not is_safe_url(url, allowed_hosts, require_https):
        messages.error(request, "You can't hack me😎😎")
        return False

    return True


class MessageMixin:
    message = ''
    message_level = messages.SUCCESS  # Default tag

    def send_message(self, request, default_messages=True):
        if default_messages is False:
            """ Delete stored messages """
            storage = messages.get_messages(request)
            storage.used = True

        messages.add_message(request=request, level=self.message_level,message=self.message)
