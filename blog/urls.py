from django.urls import path
from .views import PostListView, PostDetailView

urlpatterns = [
    path('', view=PostListView.as_view(), name='blog.list'),
    path('detail/<slug:slug>', view=PostDetailView.as_view(), name='blog.detail'),
]