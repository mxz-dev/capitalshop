from django.shortcuts import render , get_object_or_404, redirect, reverse
from shop.models import Products, ProductCategories, Cart, CartItem
from shop.forms import ContactForm
from mag.models import Post
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home_view(request):
    products = Products.objects.filter(in_stock=True).order_by('-created_at')[:4]
    posts = Post.objects.filter(is_published=True, publish_at__lt=now()).order_by('-created_at')[:3]
    return render(request, 'index.html' , {"products":products, "posts":posts})
def shop_view(request):
    products = Products.objects.filter(in_stock=True).order_by('-created_at')
    if q := request.GET.get('s'):
        products = Products.objects.filter(Q(description__contains=q) | Q(name__contains=q) , in_stock=True).order_by('-created_at')
    return render(request, 'shop/shop.html', {'products':products})
def shopitem_view(request, slug):
    product = get_object_or_404(Products, in_stock=True, slug=slug)
    return render(request, 'shop/shop-item.html', {"product": product} )
def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'we are responds you very soon.')
    return render(request, 'contact.html', {"form":form})

@login_required
def cart_view(request):
    pass
@login_required
def add_to_cart_view(request, product, quantity):
    if quantity < 1 or quantity > 200: quantity = 1
    user = User.objects.get(username=request.user)
    try:
        cart, created = Cart.objects.get_or_create(created_by=user, status="active")
        item = get_object_or_404(Products,id=product, in_stock=True)
        cart_item = CartItem.objects.filter(cart=cart, product=item).first()
        if cart_item:
            if quantity > item.stock_count:
                cart_item.quantity = item.stock_count
            else:
                cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(cart=cart, product=item, price=item.price, quantity=quantity)
        
    except Exception as e:
        return 
    return redirect(reverse("shop:home"))


@login_required
def remove_from_cart_view(request):
    pass