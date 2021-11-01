from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView
from django.views.decorators.http import require_GET

from carts.utils import send_request_to_zp
from eCommerce.utils import required_ajax
from eCommerce.mixins import MessageMixin
from eCommerce.forms import ByMeCoffeeForm
from products.models import Product


class HomeTemplateView(MessageMixin, TemplateView):
    template_name = 'eCommerce/home.html'
    message = 'WELCOME'
    message_delete_other = True


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
        print('form is valid')
        return send_request_to_zp(self.request, amount, email, description="Thanks for coffee.")
    
    def form_invalid(self, form):
        print('form is invalid')
        return super(ByMeCoffeeFormView, self).form_invalid(form)

@require_GET
@required_ajax
def search_by_ajax(request):
    query = request.GET.get('q')
    if not query:
        return JsonResponse({})

    product_name = Product.objects \
        .filter(name__icontains=query) \
        .values_list('name', flat=True)  # ToDo: Do it by search manager

    return JsonResponse(list(product_name), safe=False)
