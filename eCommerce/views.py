from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from django.views.decorators.http import require_GET

from products.models import Product
from eCommerce.utils import required_ajax
from eCommerce.mixins import MessageMixin


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
