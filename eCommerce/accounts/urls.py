from django.urls import path, reverse_lazy
from accounts import views
from django.contrib.auth import views as pw_view

app_name = 'accounts'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('confirm/', views.ConfirmView.as_view(), name='confirm'),
    path('resend-email/', views.resend_confirm_email, name='resend-email'),

    path('profile/', views.ProfileAccount.as_view(), name='profile'),
    path('profile/update-detail/', views.UserDetailUpdateView.as_view(), name='update-detail'),
    path('check_email/', views.check_email, name='check_email'),

    path('password/change/done/', pw_view.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password/change/', pw_view.PasswordChangeView.as_view(success_url=reverse_lazy('accounts:password_change_done')), name='password_change'),

    path('password/reset/', pw_view.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),
    path('password/reset/done/', pw_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', pw_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', pw_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
