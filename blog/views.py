from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

# Create your views here.
class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'post/post_list.html'
