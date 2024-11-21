from django.db import models
from django.contrib.auth.models import User 
from django.utils.text import slugify
class PostCategories(models.Model):
    category_name = models.CharField(max_length=60)
    slug = models.SlugField(null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super(PostCategories, self).save(*args, **kwargs)
    def __str__(self):
        return self.category_name
    class Meta:
        verbose_name_plural = "Post Categories"
        
class PostTags(models.Model):
    tag_name = models.CharField(max_length=60)
    slug = models.SlugField(null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.tag_name)
        super(PostTags, self).save(*args, **kwargs)
    def __str__(self):
        return self.tag_name
    class Meta:
        verbose_name_plural = "Post Tags"
        
class Post(models.Model):
    slug = models.SlugField(null=True, blank=True)
    subject = models.CharField(max_length=256)
    content = models.TextField()
    image = models.ImageField(upload_to="uploads/mag/posts/")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=1)
    tags = models.ManyToManyField(PostTags, related_name="tags")
    category = models.ForeignKey(PostCategories, on_delete=models.CASCADE) 
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_at = models.DateTimeField()
    def __str__(self):
        return self.subject
    class Meta:
        verbose_name_plural = "Posts"
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.subject)
        super(Post, self).save(*args, **kwargs)
