from django.urls.conf import path, include

from carts import views

app_name = 'carts'

urlpatterns = [
    path('', views.cart_home, name='home'),
    path('checkout/', views.CheckoutTemplateView.as_view(), name='checkout'),
    path('finalization/', views.finalization, name='finalization'),
    path('done/', views.done, name='done'),
    path('add_or_remove/', views.add_rmv_product, name='add_rmv'),
    path('remove/', views.remove, name='remove'),

    path('zarinpal/verify/', views.verify, name='zp_verify'),
]


