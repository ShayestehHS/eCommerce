from django.utils.http import is_safe_url
from django.contrib import messages


class MessageMixin:
    message = ''
    message_level = messages.SUCCESS  # Default tag
    message_delete_other = False

    def send_message(self, request):
        if self.message_delete_other is True:
            """ Delete stored messages """
            storage = messages.get_messages(request)
            storage.used = True

        messages.add_message(request=request, level=self.message_level,
                             message=self.message)


def is_valid_url(request, url, require_https=False):
    if not url:
        return False

    allowed_hosts = request.get_host()
    if not is_safe_url(url, allowed_hosts, require_https):
        messages.error(request, "You can't hack me 😎😎")
        return False

    return True


def update_session(request, cart, is_new=False):
    request.session['cart_id'] = cart.id
    request.session['cart_items'] = cart.products.count() if not is_new else 0
