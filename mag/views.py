from django.shortcuts import render, get_object_or_404
from mag.models import Post, PostCategories, PostTags
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.db.models import Q
# Create your views here.
def blog_view(request, cat=None):
    posts = Post.objects.filter(is_published=True, publish_at__lt=now()).order_by("-created_at")
    if c := cat:
        posts = posts.filter(category__category_name=c)
    if search_query := request.GET.get('search'):
        posts = Post.objects.filter(Q(subject__contains=search_query) | Q(content__contains=search_query), is_published=True, publish_at__lt=now()).order_by("-created_at")
   
    # pagination the searched and categorized posts
    paginator = Paginator(posts, 6)
    page_num = request.GET.get('page')
    try:
        page_obj = paginator.page(page_num)
    except:
        page_obj = paginator.get_page(1)
    return render(request, 'blog/blog.html', {"page_obj":page_obj})

def post_view(request, slug):
    post = get_object_or_404(Post, is_published=True, publish_at__lt=now(), slug=slug)
    return render(request, "blog/post.html", {"post":post})