"""eCommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from eCommerce import views

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('about_us/', views.AboutUs.as_view(), name='about'),
    path('contact/', views.ContactEmailCreate.as_view(), name='contact'),
    path('search_ajax/', views.search_by_ajax, name='search_ajax'),
    path('buy_me_a_coffee/', views.ByMeCoffeeFormView.as_view(), name='by_me_coffee'),

    path('admin/', admin.site.urls),
    path('products/', include('products.urls', namespace='products')),
    path('cart/', include('carts.urls', namespace='carts')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('address/', include('address.urls', namespace='address')),
    path('analytics/', include('analytics.urls', namespace='analytics')),
    path('marketing/', include('marketing.urls', namespace='marketing')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    from debug_toolbar import urls as debug_toolbar_url
    urlpatterns += [path('__debug__/', include(debug_toolbar_url))]

admin.site.site_header = "eCommerce"
admin.site.site_title = "eCommerce"
admin.site.index_title = "Admin page"
