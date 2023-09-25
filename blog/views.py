from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .forms import PostShareForm, CreateCommentForm
from .models import Post, Comment


class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'post/post_list.html'

    def get_queryset(self):
        params = self.request.GET
        if 'filter_field' and 'filter_value' in params:
            filters = {params['filter_field'] + '__icontains':params['filter_value']}
            new_context = Post.objects.filter(**filters)
            return new_context
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['params'] = self.request.GET
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['create_comment_form'] = CreateCommentForm
        context['post_share_form'] = PostShareForm
        return context

    def post(self, request:HttpRequest, *args:str, **kwargs:Any) -> HttpResponse:
        self.object = self.get_object() 
        context = self.get_context_data(**kwargs)

        if 'comment' in request.POST:
            comment_form = CreateCommentForm(request.POST)
            context['create_comment_form'] = comment_form
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = self.object
                new_comment.save()
                messages.success(self.request, 'Form submission successful', extra_tags='comment_form')
                return HttpResponseRedirect(self.object.get_absolute_url())

        if 'share' in request.POST:
            share_form = PostShareForm(request.POST)
            context['post_share_form'] = share_form    
            if share_form.is_valid():
                share_form.send_email(self.request.build_absolute_uri())
                messages.success(self.request, 'Form submission successful', extra_tags='share_form')
                return HttpResponseRedirect(self.object.get_absolute_url())
        
        
        return self.render_to_response(context)