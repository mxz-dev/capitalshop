
from django.urls import path
from . import views

app_name = "mag"
urlpatterns = [
    path("", views.blog_view , name="blog"),
    path("category/<str:cat>", views.blog_view , name="category"),
    path("post/<slug:slug>", views.post_view , name="post"),
]
