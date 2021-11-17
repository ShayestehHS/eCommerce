from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, ListView, FormView
from django.views.decorators.http import require_GET

from accounts.forms import ContactEmailForm
from carts.utils import send_request_to_zp
from eCommerce.utils import custom_send_email, required_ajax
from eCommerce.mixins import MessageMixin
from orders.forms import ByMeCoffeeForm
from orders.models import Payments
from products.models import Product

User = get_user_model()


class HomeTemplateView(MessageMixin, TemplateView):
    template_name = 'eCommerce/home.html'
    message = 'WELCOME'
    message_delete_other = True


class AboutUs(TemplateView):
    template_name = 'eCommerce/about_us.html'


class ContactEmailCreate(CreateView, MessageMixin):
    http_method_names = ['get', 'post']
    message = 'Your message is received'
    message_level = messages.SUCCESS
    form_class = ContactEmailForm
    template_name = 'accounts/contact.html'

    @method_decorator(required_ajax)
    def post(self, request, *args, **kwargs):
        return super(ContactEmailCreate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user if self.request.user.is_authenticated else None
        form.save()
        admin_email_list = User.objects.filter(is_superuser=True).values_list('email', flat=True)

        custom_send_email(
            title=f'Contact email from {form.email}',
            to=admin_email_list,
            context={'msg_model': form},
            template_name='email/contact_email.html'
        )
        return JsonResponse({})

    def form_invalid(self, form):
        self.message = 'You form is not valid'
        self.message_level = messages.ERROR
        return super(ContactEmailCreate, self).form_invalid(form)

    def get_initial(self):
        user = self.request.user if self.request.user.is_authenticated else None
        if user is None:
            return super(ContactEmailCreate, self).get_initial()

        return {'email': user.email, 'full_name': user.full_name}


class SearchProductListView(ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q')
        if not query:
            return Product.objects.none()

        return Product.objects.search(query)


class ByMeCoffeeFormView(FormView):
    form_class = ByMeCoffeeForm
    template_name = 'eCommerce/by_me_caffe.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = self.request.user
        form.user = user if user.is_authenticated else None
        form.save()
        email = form.cleaned_data.get('email')
        full_name = form.cleaned_data.get('full_name')
        amount = form.cleaned_data.get('amount')
        Payments.objects.get_or_create(full_name=self.request.user.full_name,
                                       user=self.request.user, amount=amount)
        return send_request_to_zp(self.request, amount, email, description="Thanks for coffee.")

    def form_invalid(self, form):
        messages.error(self.request, 'Your form is invalid.')
        return super(ByMeCoffeeFormView, self).form_invalid(form)


@require_GET
@required_ajax
def search_by_ajax(request):
    query = request.GET.get('q')
    if not query:
        return JsonResponse({})

    product_name = Product.objects \
        .filter(name__icontains=query) \
        .values_list('name', flat=True)

    return JsonResponse(list(product_name), safe=False)
