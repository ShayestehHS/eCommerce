from django.views.generic import ListView, DetailView

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
    queryset = Product.objects.all()
    context_object_name = 'product'
