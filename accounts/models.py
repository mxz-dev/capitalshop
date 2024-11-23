from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, Permission
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import validators
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class CustomUser(AbstractBaseUser):
    username_validator = validators.ASCIIUsernameValidator()
    username = models.CharField(
        max_length=100, 
        unique=True, 
        validators=[username_validator],
        help_text = ("Required. 150 characters or fewer. Letters, digits and symbols only."),
        error_messages = {
            'unique': ("A user with that username already exists."),
        },
        )
    email = models.EmailField(
        max_length=200,
        unique=True,
        help_text = ("Required. 150 characters or fewer."),
        error_messages = {
            'unique': ("A email with that email already exists."),
        },
        )
    password = models.CharField(max_length=1200)
    is_active = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, help_text = ("your first name"))
    last_name = models.CharField(max_length=100, help_text = ("your last name"))
    address = models.CharField(max_length=250)
    phone_number = PhoneNumberField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()
        
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    class Meta:
        verbose_name_plural = "Custom Users"