from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(PostTags, PostCategories)
class TagsAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    search_fields = ['subject', 'content']
    list_filter = ['is_published', 'category']
    ordering = ['created_at']
    empty_value_display = '-empty-'
    


