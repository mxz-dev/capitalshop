from django import forms
from captcha.fields import CaptchaField
from shop.models import Contact, Checkout

class ContactForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Contact
        fields = "__all__"

class CheckoutForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Checkout
        fields = "__all__"
        exclude = ("created_by","user_id","cart","order", "payment_status", "total_amount")