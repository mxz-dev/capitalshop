from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Set a unique related name here
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",  # Set a unique related name here
        blank=True
    )
    address = models.CharField(max_length=250)
    phone_number = PhoneNumberField(blank=True)