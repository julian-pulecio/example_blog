from django.urls import path
from .views import PostListView, PostDetailView, PostListFiltersView, CommentSectionView 

urlpatterns = [
    path('', view=PostListView.as_view(), name='blog.list'),
    path('filter', view=PostListFiltersView.as_view(), name='blog.filter'),
    path('detail/<slug:slug>', view=PostDetailView.as_view(), name='blog.detail'),
    path('comments/<slug:slug>', view=CommentSectionView.as_view(), name='blog.comments'),
]