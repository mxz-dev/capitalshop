from django.contrib import admin
from .models import DeliveryInfo, PaymentInfo

admin.site.register(DeliveryInfo)
admin.site.register(PaymentInfo)
