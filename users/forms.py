from django import forms #type: ignore
from django.contrib.auth.forms import UserCreationForm #type: ignore
from users.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
