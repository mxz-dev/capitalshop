from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Orders, OrderLine)
class OrdersAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    empty_value_display = '-empty-'

@admin.register(Cart, CartItem)
class CartAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    empty_value_display = '-empty-'

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_filter = ['category', 'discount_type']
    search_fields = ['name', 'description']
    ordering = ['created_at']
    empty_value_display = '-empty-'
@admin.register(Contact)
class ContactsAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    ordering = ['created_at']
    search_fields = ['message']
    empty_value_display = '-empty-'
@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    empty_value_display = '-empty-'
    ordering = ['created_at']
    list_filter = ['is_approved', 'product']    
    search_fields = ['comment']
admin.site.register(ProductCategories)
