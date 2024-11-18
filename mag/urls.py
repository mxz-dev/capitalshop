
from django.urls import path
from . import views

app_name = "mag"
urlpatterns = [
    path("", views.blog_view , name="blog"),
    path("post/<slug:slug>", views.post_view , name="post"),
]
