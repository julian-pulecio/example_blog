from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from .forms import PostShareForm
from .models import Post

# Create your views here.
class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'post/post_list.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'

class PostShareView(FormView):
    form_class = PostShareForm
    template_name = 'post/post_share.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        get_object_or_404(Post, slug=kwargs['slug'])
        return super().get(request, *args, **kwargs)

    def form_valid(self, form) -> HttpResponse:
        form.send_email(self.request.build_absolute_uri())
        messages.success(self.request, 'Form submission successful')
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.request.get_full_path()