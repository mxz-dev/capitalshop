from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()
    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

class CustomAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField()
    class Meta:
        model = CustomUser
        fields = ("username", "password")
