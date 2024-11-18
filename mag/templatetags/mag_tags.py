from django import template
from mag.models import PostCategories, Post
from django.utils.timezone import now
register = template.Library()
@register.inclusion_tag("inc/categories.html")
def categories():
    categories = PostCategories.objects.all()
    if categories.count() > 15:
        categories = categories[:15]
    return {'categories':categories}
@register.inclusion_tag('inc/popular_posts.html')
def popular_posts():
    posts = Post.objects.filter(is_published=True, publish_at__lt=now()).order_by("-views")
    return {"posts":posts[:3]}