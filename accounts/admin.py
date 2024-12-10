from django.contrib import admin
from django import forms 
from .models import DeliveryInfo, PaymentInfo

admin.site.register(DeliveryInfo)

class CustomPaymentInfoForm(forms.ModelForm):
    class Meta:
        model = PaymentInfo
        widgets = {
            'card_number': forms.NumberInput(attrs={'class':'form-control','id':'cardNumber', 'maxlength':16})
        }
        fields = "__all__"

class PaymentInfoAdmin(admin.ModelAdmin):
    form = CustomPaymentInfoForm
    date_hierarchy = 'created_at'
    list_filter = ['user']
    search_fields = ['user', 'card_number']
    ordering = ['created_at']
    empty_value_display = '-empty-'

admin.site.register(PaymentInfo,PaymentInfoAdmin)
