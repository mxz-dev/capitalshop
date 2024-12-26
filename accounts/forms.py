from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from accounts.models import PaymentInfo, DeliveryInfo
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

class UpdateProfileForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name",)
        exclude = ["username", "password"]

class PaymentInfoForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = PaymentInfo
        fields = ("card_number","expiry_date", "cvv")
class DeliveryInfoForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = DeliveryInfo
        fields = ("address", "phone_number")
    

class UpdateUserPasswordForm(forms.Form):
    captcha = CaptchaField()
    current_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    new_password_confirm = forms.CharField(widget=forms.PasswordInput())