from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager

# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = ('PB','Published')
        DRAFT = ('DF','Draft')

    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    status = models.CharField(choices=Status.choices, default=Status.DRAFT, max_length=2)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(max_length=255)
    tags = TaggableManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog.detail',args=[self.slug])
    
    def save(self,*args,**kwargs):
        self.slug=slugify(self.title)
        super(Post,self).save(*args,**kwargs)
