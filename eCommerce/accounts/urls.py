from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', views.logout, name='logout'),
    path('contact/', views.ContactEmailCreate.as_view(), name='contact'),
    path('login/', views.Login.as_view(), name='login'),
    path('check_email/', views.check_email, name='check_email'),
]
