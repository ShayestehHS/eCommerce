from django.urls import path

from address import views

app_name = 'address'

urlpatterns = [
    path('use/', views.address_use, name='use'),
    path('list/', views.AddressListView.as_view(), name='list'),
    path('ajax_list/', views.ajax_list_address, name='ajax_list'),
    path('update/<int:pk>/', views.AddressUpdateView.as_view(), name='update'),
    path('set_address/', views.AddressCreateView.as_view(), name='set_address'),
]
