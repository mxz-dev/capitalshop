
from django.urls import path, re_path
from . import views


app_name = 'accounts'
urlpatterns = [
    path("login", views.login_view , name="login"),
    path("signup", views.registration_view , name="registration"),
    path("signout", views.signout, name="signout"),
    path("profile", views.update_profile_view, name="dashboard"),
    path("billing", views.billing_view , name="billing"),
    path("security", views.security_view , name="security"),
    path("activate/<slug:uidb64>/<slug:token>", views.activation_view, name='activate'),
    path('billing/card/add', views.add_credit_card, name="add_credit_card"),
    path('billing/info/add', views.add_delivery_info, name='add_delivery_info'),
    path("billing/card/delete/<int:pk>", views.delete_card, name="delete_card"),
    path("billing/info/delete/<int:pk>", views.delete_address, name="delete_info"),

]
