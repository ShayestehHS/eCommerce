from django.urls.conf import path

from products import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('digitals/', views.DigitalProductListView.as_view(), name='digital_list'),
    path('history/', views.UserProductHistoryListView.as_view(), name='history'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),

]
