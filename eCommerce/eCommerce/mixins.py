from django.contrib import messages
from django.urls import reverse_lazy

from eCommerce.utils import is_valid_url


class BootstrapFieldsForm(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self.fields
        for field in fields:
            fields[field].widget.attrs.update({'class': 'form-control'})


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


class NextUrlMixin(object):
    default_next = reverse_lazy('home')

    def get_success_url(self):
        request = self.request
        next_url_get = request.GET.get('next')
        next_url_post = request.POST.get('next')
        redirect_path = next_url_get or next_url_post or None
        if not is_valid_url(request, redirect_path):
            return self.default_next
        return redirect_path


class RequestFormAttachMixin(object):

    def __init__(self):
        super(RequestFormAttachMixin, self).__init__()
        print('request form attach mixin')

    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
