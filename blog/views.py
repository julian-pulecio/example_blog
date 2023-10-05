from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView, FormView, View
from django.db.models import Q
from .forms import PostFilterListForm, CreateCommentForm
from .models import Post, Comment


class PostListFiltersView(FormView):
    template_name = 'post/post_list_filters.html'
    form_class = PostFilterListForm

class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'post/post_list.html'

    def get_queryset(self):
        tags_filter = self.request.GET.get('tags_filter')
        title_filter = self.request.GET.get('title_filter')

        filters = False
        query = Q()
        
        if tags_filter is not None and len(tags_filter):
            query &= Q(tags__name=tags_filter)
            filters = True

        if title_filter is not None and len(title_filter):
            query &= Q(title__icontains=title_filter)
            filters = True

        if filters:
            new_context = Post.objects.filter(query)
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
        context['slug'] = self.kwargs['slug']
        return context

class CommentSectionView(TemplateView):
    template_name = 'post/post_comment_section.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Comment.objects.filter(post__slug=kwargs['slug'])
        context['form'] = CreateCommentForm
        return context

    def post(self, request, *args, **kwargs):
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.filter(slug=kwargs['slug'])[0]
            comment.save()
            return HttpResponseRedirect(reverse('blog.comments', args=[kwargs['slug']]))
        return render(
            request, self.template_name, {
                'form': form,
                'slug':kwargs['slug'],
                'object_list': Comment.objects.filter(post__slug=kwargs['slug'])
            })