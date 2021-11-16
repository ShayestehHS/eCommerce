from functools import wraps

from django.core.exceptions import BadRequest
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import is_safe_url
from django.utils.html import strip_tags
from django.contrib import messages
from django.template.loader import render_to_string


def custom_send_email(title, to, context, template_name):
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    send_mail(title, plain_message, settings.EMAIL_HOST_USER, to, html_message=html_message)


def is_valid_url(request, url, require_https=False):
    if not url:
        return False

    allowed_hosts = request.get_host()
    if not is_safe_url(url, allowed_hosts, require_https):
        messages.error(request, "You can't hack me 😎😎")
        return False

    return True


def update_session(request, cart, is_new=False):
    session_id = request.session.get('cart_id', 0)
    cart_id = cart.id
    if is_new or session_id != cart_id:
        request.session['cart_id'] = cart_id
        request.session['cart_items'] = cart.products.count()


def required_ajax(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if not request.is_ajax():
            raise BadRequest('Request is not AJAX.')

        return view(request, *args, **kwargs)

    return _wrapped_view


def get_next_url(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        next_url_get = request.GET.get('next')
        next_url_post = request.POST.get('next')
        redirect_path = next_url_get or next_url_post
        if not is_valid_url(request, redirect_path):
            kwargs['next_url'] = None

        kwargs['next_url'] = redirect_path
        return view(request, *args, **kwargs)

    return _wrapped_view
