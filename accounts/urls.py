
from django.urls import path, re_path
from . import views


app_name = 'accounts'
urlpatterns = [
    path("login", views.login_view , name="login"),
    path("signup", views.registration_view , name="registration"),
    path("signout", views.signout, name="signout"),
    path("dashboard", views.dashboard_view, name="dashboard"),
    path('activate/<slug:uidb64>/<slug:token>', views.activation_view, name='activate'),
]
