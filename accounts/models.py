from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField


def validate_16_digits(value):
    if len(str(value)) != 16:
        raise ValidationError(f'The number must have exactly 16 digits, but {value} has {len(str(value))} digits.')

def validate_3_or_4_digits(value):
    if len(str(value)) < 3 and len(str(value)) > 5:
        raise ValidationError(f'The number must have 3 or 4 digits, but {value} has {len(str(value))} digits.')

class DeliveryInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=400)
    phone_number = PhoneNumberField(null=True)
    def __str__(self):
        return f"delivery info for {self.user.username}"
    class Meta:
        verbose_name_plural = "Delivery Info"
class PaymentInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    card_number = models.IntegerField(validators=[validate_16_digits] ) # 16 digit
    expiry_date = models.DateField()
    cvv = models.IntegerField(validators=[validate_3_or_4_digits])    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        c = str(self.card_number)
        return f"****-****-****-{c[:4]} for {self.user.username} "
    class Meta:
        verbose_name_plural = "Payment Info"