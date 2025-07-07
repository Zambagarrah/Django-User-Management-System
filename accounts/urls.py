from django.urls import path
from .views import (
    register_view, profile_view, edit_profile,
    change_password, verify_user
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('change-password/', change_password, name='change_password'),
    path('verify/', verify_user, name='verify_user'),
]