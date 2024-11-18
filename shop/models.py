from django.db import models
from accounts.models import CustomUser
from django.utils.text import slugify


STATUS = (
    ("ordered", "ordered"),
    ("active", "active"),
    ("abandoned", "abandoned")
)

class ProductCategories(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super(ProductCategories, self).save(*args, **kwargs)
    def __str__(self):
        return self.category_name
    class Meta:
        verbose_name_plural = "ProductCategories"

class Products(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to="uploads/shop/products/")
    description = models.TextField(max_length=550)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE, related_name="products")
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Products, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Products"
class Cart(models.Model):
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="carts")
    status = models.CharField(choices=STATUS, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'Cart by {self.created_by.get_full_name}'
    class Meta:
        verbose_name_plural = "Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="cart_items")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Cart Items by {self.cart.created_by.get_full_name}'
    class Meta:
        verbose_name_plural = "Cart Items"
class Orders(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Orders"
class OrderLine(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="order_lines")
    products = models.ManyToManyField(Products, related_name="order_lines")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="wishlists")
    created_at = models.DateTimeField(auto_now_add=True)

class Reviews(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="reviews")
    comment = models.CharField(max_length=300)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Review by {self.user.get_full_name}'
    class Meta:
        verbose_name_plural = "Reviews"
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=256)
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Message from {self.name}'
    class Meta:
        verbose_name_plural = "Contacts"