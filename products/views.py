from django.shortcuts import render
from django.views.generic import ListView, DetailView

from products.models import Product


class ProductListView(ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    context_object_name = 'product'
