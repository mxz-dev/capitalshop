from django.contrib import admin
from .models import CustomUser
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ("username", "first_name", "last_name", "email")
    list_filter = ['is_active']
    list_display = ("username", "email", "first_name", "last_name", "is_active")
    ordering = ['username']
    empty_value_display = '-empty-'