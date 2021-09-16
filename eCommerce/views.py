from django.views.generic import TemplateView, ListView

from products.models import Product


class HomeTemplateView(TemplateView):
    template_name = 'eCommerce/home.html'


class SearchProductListView(ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q')
        if query is None:
            return Product.objects.none()

        return Product.objects.search(query)
