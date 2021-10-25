from django.urls import path

from address import views

app_name = 'orders'

urlpatterns = [
    path('list/', views.AddressListView.as_view(), name='list'),
    path('use/', views.address_use, name='use'),
]
