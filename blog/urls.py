from django.urls import path
from .views import PostListView, PostDetailView, PostShareView, CreateCommentView

urlpatterns = [
    path('', view=PostListView.as_view(), name='blog.list'),
    path('detail/<slug:slug>', view=PostDetailView.as_view(), name='blog.detail'),
    path('share/<slug:slug>', view=PostShareView.as_view(), name='blog.share'),
    path('comment/<slug:slug>', view=CreateCommentView.as_view(), name='blog.comment'),
]