from django.urls import path

from address import views

app_name = 'orders'

urlpatterns = [
    path('address/list/', views.AddressListView.as_view(), name='address_list'),
]