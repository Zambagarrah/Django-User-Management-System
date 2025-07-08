from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


User = get_user_model()


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'full_name', 'bio', 'location']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
