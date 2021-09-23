from django.urls.conf import path, include

from carts import views

app_name = 'carts'

urlpatterns = [
    path('', views.cart_home, name='home'),
    path('checkout/', views.checkout, name='checkout'),
    path('finalization/', views.finalization, name='finalization'),
    path('delete_product/', views.remove_product, name='remove_product'),
    path('add_product/', views.add_product, name='add_product'),
    path('create_address/', views.set_address_to_order, name='address_create'),
]
