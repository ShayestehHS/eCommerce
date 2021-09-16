from django.urls.conf import path, include

from carts import views

app_name = 'carts'

urlpatterns = [
    path('', views.cart_home, name='cart'),
]
