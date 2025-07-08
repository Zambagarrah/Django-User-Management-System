from django.urls import path
from .views import (
    register_view, profile_view, edit_profile,
    change_password, verify_user, home_view
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('change-password/', change_password, name='change_password'),
    path('verify/', verify_user, name='verify_user'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]