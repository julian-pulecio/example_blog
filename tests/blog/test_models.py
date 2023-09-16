import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestPostModel:
    def test_str_return(self, post_factory):
        post = post_factory(title='post_title')
        assert post.__str__() == 'post_title'
    
    def test_absolute_url(self, post_factory):
        post = post_factory(title='post title')
        assert post.get_absolute_url() == reverse('blog.detail', args=['post-title'])