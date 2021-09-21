from django.views.generic import ListView, DetailView

from carts import utils
from products.models import Product


class ProductListView(ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'

    def get_queryset(self):
        queryset = self.queryset \
            .prefetch_related('tagged_items') \
            .defer('is_featured', 'is_active', 'timestamp')

        return queryset


class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    queryset = Product.objects.all()

    def get_queryset(self):
        qs = self.queryset.defer('is_active', 'slug')
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        cart = utils.get_cart_from_session(self.request)
        context['in_cart'] = self.object.id in cart.products.all_id()
        return context
