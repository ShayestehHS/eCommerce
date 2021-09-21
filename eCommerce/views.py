from django.views.generic import TemplateView, ListView

from products.models import Product
from eCommerce.utils import MessageMixin


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
        if query is None:
            return Product.objects.none()

        return Product.objects.search(query)
