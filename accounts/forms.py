from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import CustomUser
from .backends.auth_backend import AuthBackend
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
    def clean(self):
        """Add custom authentication logic if needed."""
        cleaned_data = super().clean()
        username = self.cleaned_data.get('username')  # 'username' is the field used by `AuthenticationForm`
        password = self.cleaned_data.get('password')
        
        # Custom authentication logic if needed
        user = AuthBackend().authenticate(self.request, username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid login credentials", code='invalid_login')
        return cleaned_data
