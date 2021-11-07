import hashlib
import re

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

MAILCHIMP_API_KEY = getattr(settings, "MAILCHIMP_API_KEY")
MAILCHIMP_DATA_CENTER = getattr(settings, "MAILCHIMP_DATA_CENTER")
MAILCHIMP_PUB_KEY = getattr(settings, "MAILCHIMP_PUB_KEY")


def check_valid_status(status):
    valid_status = ["subscribed", "unsubscribed", "pending", "cleaned"]
    if status not in valid_status:
        raise ValueError("Invalid status")
    return status


def get_hashed_email(email):
    if not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email):
        raise ValueError('Invalid email address')

    return hashlib.md5(email.encode('utf-8').lower()).hexdigest()


class Mailchimp(object):
    def __init__(self, api_key=MAILCHIMP_API_KEY, list_id=MAILCHIMP_PUB_KEY, dc=MAILCHIMP_DATA_CENTER):
        self.mailchimp = Client()
        self.list_id = list_id

        self.mailchimp.set_config({"api_key": api_key, "server": dc})
        super(Mailchimp, self).__init__()

    def get_subscription_status(self, email):
        member_email_hash = get_hashed_email(email)

        try:
            response = self.mailchimp.lists.get_list_member(self.list_id, member_email_hash)

        except ApiClientError as error:
            # Based on documentation: 'If the call returns an error response, the contact is not on the list.'
            return 'unsubscribed'

        return response.get('status')

    def subscribe(self, email, **kwargs):
        email_status = self.get_subscription_status(email)
        if email_status == "subscribed":
            # print(f"{email} is already a list member")
            return True

        member_info = {"email_address": email, "status": "subscribed"}
        try:
            response = self.mailchimp.lists.add_list_member(self.list_id, member_info)

        except ApiClientError as error:
            # Access denied? => Turn on vpn
            raise Exception(f"An exception occurred: {error.text}")

        return response.get('status') == "subscribed"

    def change_status(self, email, status):
        check_valid_status(status)

        hashed_email = get_hashed_email(email)
        member_update = {"status": status}

        try:
            response = self.mailchimp.lists.update_list_member(self.list_id, hashed_email, member_update)
        except ApiClientError as error:
            raise Exception(f"An exception occurred: {error.text}")

        return response.get('status') == status


# ToDo: What is this?, What is the object in classes?, What is the method_decorator?,
# ToDo: What is the python module?
class CsrfExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(request, *args, **kwargs)
