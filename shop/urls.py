
from django.urls import path
from . import views
app_name = 'shop'
urlpatterns = [
    path("", views.home_view , name="home"),
    path("shop", views.shop_view , name="shop"),
    path("product/<slug:slug>", views.shopitem_view, name="shopitem"),
]
