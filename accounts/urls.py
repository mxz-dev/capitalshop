
from django.urls import path, re_path
from . import views


app_name = 'accounts'
urlpatterns = [
    path("login", views.login_view , name="login"),
    path("signup", views.registration_view , name="registration"),
    path("signout", views.signout, name="signout"),
    path("profile", views.dashboard_view, name="dashboard"),
    path("billing", views.billing_view , name="billing"),
    path("security", views.security_view , name="security"),
    path('activate/<slug:uidb64>/<slug:token>', views.activation_view, name='activate'),
    path("card/add/", views.add_card, name="add_card"),
    path("card/edit/<int:pk>", views.edit_card, name="edit_card"),
    path("card/delete/<int:pk>", views.delete_card, name="delete_card"),

]
