from django.shortcuts import render
from mag.models import Post, PostCategories, PostTags
from django.utils.timezone import now
# Create your views here.
def blog_view(request):
    posts = Post.objects.filter(is_published=True, publish_at__lt=now()).order_by("-created_at").exclude(pin=True)
    pinned_post = Post.objects.filter(is_published=True, publish_at__lt=now(),pin=True).order_by("pin","-created_at").first()
    return render(request, 'blog/blog.html', {"posts":posts, "pin_post":pinned_post})
def post_view(request, slug):
    pass