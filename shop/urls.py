
from django.urls import path
from . import views
app_name = 'shop'
urlpatterns = [
    path("", views.home_view , name="home"),
    path("shop", views.shop_view , name="shop"),
    path("product/<slug:slug>", views.shopitem_view, name="shopitem"),
    path("about", views.about_view, name="about"),
    path("contact", views.contact_view, name="contact"),
    path("cart", views.cart_view, name="cart"),
    path("cart/add/<str:product>/<int:quantity>", views.add_to_cart_view, name="add_to_cart"),
    path("cart/remove/<str:product>", views.remove_from_cart_view, name="remove_from_cart"),

]
