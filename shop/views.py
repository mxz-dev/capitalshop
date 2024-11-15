from django.shortcuts import render
from shop.models import Products

def home_view(request):
    products = Products.objects.filter(in_stock=True).order_by('-created_at')
    return render(request, 'index.html' , {"products":products[:3]})

def shop_view(request):
    return render(request, 'shop/shop.html')
