
from django.urls import path, re_path
from . import views
app_name = 'shop'
urlpatterns = [
    path("", views.home_view , name="home"),
    path("shop", views.shop_view , name="shop"),
    path("product/<slug:slug>", views.shopitem_view, name="shopitem"),
    path("about", views.about_view, name="about"),
    path("contact", views.contact_view, name="contact"),
    path("cart", views.cart_view, name="cart"), # read
    path("cart/add/<int:product>/<int:quantity>", views.add_item_to_cart, name="add_to_cart"), # create
    path("cart/remove/<int:product>", views.remove_item, name="remove_from_cart"), # delete
    re_path(r'^cart/update/(?P<product>\d+)/(?P<quantity>-?\d+)/$', views.update_cart_item_quantity, name='update_cart_item_quantity'),
    path("checkout", views.checkout_view, name="checkout"),
]
