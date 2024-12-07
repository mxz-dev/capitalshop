from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class DeliveryInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=400)
    phone_number = PhoneNumberField(null=True)
    def __str__(self):
        return f"info for {self.user.username}"
    class Meta:
        verbose_name_plural = "Delivery Info"