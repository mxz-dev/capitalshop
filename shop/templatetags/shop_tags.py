from django import template
from shop.models import ProductCategories, Products
from django.shortcuts import get_object_or_404
register = template.Library()

@register.inclusion_tag('inc/related_product.html')
def show_related_products(slug):
    product = get_object_or_404(Products, in_stock=True, slug=slug)
    products = Products.objects.filter(in_stock=True, category=product.category)
    products = products.exclude(slug=product.slug)
    return {"products":products}