from django.urls import path
from .views import PostListView

urlpatterns = [
    path('', view=PostListView.as_view(), name='blog.list')
]