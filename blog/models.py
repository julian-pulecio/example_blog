from django.db import models

# Create your models here.
class Blog(models.Model):
    
    class Status(models.TextChoices):
        PUBLISHED = ('PB','Published')
        DRAFT = ('DF','Draft')

    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    status = models.CharField(choices=Status.choices, default=Status.DRAFT, max_length=2)

    def __str__(self):
        return self.title
