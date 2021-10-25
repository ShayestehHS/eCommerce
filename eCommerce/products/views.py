from django.views.generic import ListView, DetailView

from analytics.mixins import ObjectViewedMixin
from carts import utils
from carts.models import Cart
from products.models import Product


class ProductListView(ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'
    template_name = 'products/product_list.html'

    def get_queryset(self):
        queryset = self.queryset \
            .prefetch_related('tagged_items') \
            .defer('is_featured', 'is_active', 'timestamp')

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        try:
            cart = Cart.objects.get(user=self.request.user, is_active=True)
            context['all_id'] = cart.products.all_id()
        except (Cart.DoesNotExist, TypeError) as e:
            pass
        return context


class ProductDetailView(ObjectViewedMixin, DetailView):
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    queryset = Product.objects.all()

    def get_queryset(self):
        qs = self.queryset.defer('is_active', 'slug')
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        cart = utils.get_cart_from_session(self.request)
        context['in_cart'] = self.object.id in cart.products.all_id()
        return context
