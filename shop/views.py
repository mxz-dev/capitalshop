from django.shortcuts import render , get_object_or_404, redirect, reverse, HttpResponse
from shop.models import Products, ProductCategories, Cart, CartItem
from shop.forms import ContactForm
from mag.models import Post
from django.contrib.auth.models import User
from django.http import JsonResponse
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
    user = request.user
    cart = get_object_or_404(Cart,created_by=user, status="active")
    cart_item = CartItem.objects.filter(cart=cart)
    total_price = 0
    for item in cart_item:
        if item.quantity > 1:
            total_price += item.quantity * item.price 
        else:
            total_price += item.price 
    return render(request,'shop/cart.html', {"cart_items":cart_item, "total_price":total_price})

@login_required
def add_item_to_cart(request, product, quantity):
    user = request.user
    cart, created = Cart.objects.get_or_create(created_by=user, status="active")

    # Ensure the product exists and is in stock
    item = get_object_or_404(Products, id=product, in_stock=True)

    # Check if the item is already in the cart
    cart_item = CartItem.objects.filter(cart=cart, product=item).first()

    if cart_item:
        # Check if the requested quantity exceeds stock availability
        if cart_item.quantity + quantity > item.stock_count:
            cart_item.quantity = item.stock_count
        else:
            cart_item.quantity += quantity
        cart_item.save()
    else:
        # Ensure the requested quantity does not exceed stock availability
        quantity = min(quantity, item.stock_count)
        cart_item = CartItem.objects.create(cart=cart, product=item, price=item.price, quantity=quantity)
    messages.add_message(request, messages.SUCCESS, f"{cart_item.product.name} added to cart.")
    return redirect(reverse("shop:shopitem", kwargs={'slug':item.slug}))

@login_required
def remove_item(request, product):
    user = request.user # get current user

    # ensure cart is exists.
    cart = get_object_or_404(Cart, created_by=user)

    # Find the item to remove from the cart
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    # Remove the item from the cart
    cart_item.delete()
    return JsonResponse({
        "message": "item removed from cart.",
     })


@login_required
def update_cart_item_quantity(request, product, quantity):
    quantity = int(quantity) 
    user = request.user
    
    # ensure cart is exists.
    cart = get_object_or_404(Cart, created_by=user)
    
    # find the item to update from the cart.
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    # calculate new quantity
    new_quantity = cart_item.quantity + quantity
    if new_quantity < 1:
        cart_item.delete()  # Remove the item from the cart if quantity drops below 1
        return JsonResponse({"message": "Item removed from cart."})
    elif new_quantity > cart_item.product.stock_count:
        cart_item.quantity = cart_item.product.stock_count  # Cap at available stock
    else:
        cart_item.quantity = new_quantity  # Update to the new quantity

    cart_item.save()
    return JsonResponse({
        "message": "Quantity updated successfully.",
        "quantity": cart_item.quantity
    })
