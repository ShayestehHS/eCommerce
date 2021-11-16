from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('detail/<int:pk>/', views.OrderAccountDetail.as_view(), name='detail'),
    path('list/', views.OrderAccountList.as_view(), name='list'),
]
