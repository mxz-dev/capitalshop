from django.shortcuts import render, get_object_or_404
from mag.models import Post, PostCategories, PostTags
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now
from django.db.models import Q
# Create your views here.
def blog_view(request, cat=None):
    posts = Post.objects.filter(is_published=True, publish_at__lt=now()).order_by("-created_at").exclude(pin=True)
    pinned_post = Post.objects.filter(is_published=True, publish_at__lt=now(),pin=True).order_by("pin","-created_at").first()
    if c := cat:
        posts = Post.objects.filter(is_published=True, publish_at__lt=now(),category__category_name=c).order_by("-created_at")
        pinned_post = None
    if search_query := request.GET.get('search'):
        posts = Post.objects.filter(Q(subject__contains=search_query) | Q(content__contains=search_query),is_published=True, publish_at__lt=now() ).order_by("-created_at")
        pinned_post = None

    paginator = Paginator(posts, 4)
    page_num = request.GET.get('page')
    try:
        page_obj = paginator.page(page_num)
    except EmptyPage:
        page_obj = paginator.page(1)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    
    return render(request, 'blog/blog.html', {"page_obj":page_obj, "pin_post":pinned_post})

def post_view(request, slug):
    post = get_object_or_404(Post, is_published=True, publish_at__lt=now(), slug=slug)
    return render(request, "blog/post.html", {"post":post})