from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, FormView, CreateView
from .forms import PostShareForm, CreateCommentForm
from .models import Post, Comment



# Create your views here.
class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'post/post_list.html'

class PostDetailView(FormMixin,DetailView):
    model = Post
    form_class = CreateCommentForm
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

class CreateCommentView(CreateView):
    model = Comment
    form_class = CreateCommentForm

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs.get('slug'))
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, post)
        return self.form_invalid(form)

    def get_success_url(self, post:Post) -> str:
        return post.get_absolute_url()

    def form_valid(self, form, post:Post) -> HttpResponse:
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())