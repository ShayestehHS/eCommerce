from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('detail/<int:pk>/', views.OrderAccountDetail.as_view(), name='detail'),
    path('set_address/', views.set_address_to_order, name='set_address'),
    path('list/', views.OrderAccountList.as_view(), name='list'),
]
