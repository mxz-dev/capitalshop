from django.shortcuts import render, get_object_or_404
from mag.models import Post, PostCategories, PostTags
from django.utils.timezone import now
# Create your views here.
def blog_view(request, cat=None):
    posts = Post.objects.filter(is_published=True, publish_at__lt=now()).order_by("-created_at").exclude(pin=True)
    pinned_post = Post.objects.filter(is_published=True, publish_at__lt=now(),pin=True).order_by("pin","-created_at").first()
    if c := cat:
        posts = Post.objects.filter(is_published=True, publish_at__lt=now(),category__category_name=c).order_by("-created_at")
        pinned_post = None
    return render(request, 'blog/blog.html', {"posts":posts, "pin_post":pinned_post})
def post_view(request, slug):
    post = get_object_or_404(Post, is_published=True, publish_at__lt=now(), slug=slug)
    return render(request, "blog/post.html", {"post":post})