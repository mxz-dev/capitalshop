from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *
# Register your models here.


@admin.register(PostTags, PostCategories)
class TagsAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostsAdmin(SummernoteModelAdmin):
    search_fields = ['subject', 'content']
    summernote_fields = ('content',)
    list_filter = ['is_published', 'category']
    ordering = ['created_at']
    empty_value_display = '-empty-'
    


