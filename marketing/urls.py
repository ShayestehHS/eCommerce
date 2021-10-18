from django.urls import path

from marketing import views

app_name = 'marketing'

urlpatterns = [
    path('subscription/', views.UpdateSubscription.as_view(), name='subscription'),
]
