from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

class CustomAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ("username", "password")
