from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('confirm/', views.ConfirmView.as_view(), name='confirm'),
    path('resend-email/', views.resend_confirm_email, name='resend-email'),

    path('profile/', views.ProfileAccount.as_view(), name='profile'),
    path('profile/update-detail/', views.UserDetailUpdateView.as_view(), name='update-detail'),
    path('check_email/', views.check_email, name='check_email'),
]
