from django.urls import path
from .views import PostListView, PostDetailView, PostShareView

urlpatterns = [
    path('', view=PostListView.as_view(), name='blog.list'),
    path('detail/<slug:slug>', view=PostDetailView.as_view(), name='blog.detail'),
    path('share/<slug:slug>', view=PostShareView.as_view(), name='blog.share')
]