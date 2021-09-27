from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from django.views.decorators.http import require_GET
from django.core.serializers import serialize

from products.models import Product
from eCommerce.utils import MessageMixin, required_ajax


class HomeTemplateView(TemplateView, MessageMixin):
    template_name = 'eCommerce/home.html'
    message = 'WELCOME'
    message_delete_other = True

    def get_context_data(self, **kwargs):
        super(HomeTemplateView, self).get_context_data()
        self.send_message(self.request)


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
    "specific_value"
    product_name = Product.objects \
        .filter(name__icontains=query) \
        .values_list('name', flat=True) # ToDo: clean this shit

    return JsonResponse(list(product_name), safe=False)
