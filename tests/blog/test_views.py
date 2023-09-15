import pytest
from django.urls import reverse
from blog.factory import PostFactory

@pytest.fixture()
def setup_five_items():
    _ = PostFactory.create_batch(5)

@pytest.fixture()
def setup_one_hundred_items():
    _ = PostFactory.create_batch(100)


@pytest.mark.django_db
class TestPostListView:
    def test_view_returns_200_status_code(self, client):
        response = client.get(reverse('blog.list'))
        assert response.status_code == 200
    
    def test_view_uses_the_correct_template(self, client):
        response = client.get(reverse('blog.list'))
        assert 'post/post_list.html' in [ template.name for template in response.templates]
    
    def test_view_pagination_for_five_post(self, client, setup_five_items):
        response = client.get(reverse('blog.list'), {'page': '1'})
        assert len(response.context.get('object_list')) == 5
        assert 'Page 1 of 1' in response.content.decode()
        assert 'next' not in response.content.decode()
        assert 'previous' not in response.content.decode()
    
    def test_view_pagination_for_one_hundred_post(self, client, setup_one_hundred_items):
        response = client.get(reverse('blog.list'), {'page': '2'})
        assert len(response.context.get('object_list')) == 10
        assert 'Page 2 of 10.' in response.content.decode()
        assert 'next' in response.content.decode()
        assert 'previous' in response.content.decode()

        response = client.get(reverse('blog.list'), {'page': '1'})
        assert 'Page 1 of 10.' in response.content.decode()
        assert 'next' in response.content.decode()
        assert 'previous' not in response.content.decode()

        response = client.get(reverse('blog.list'), {'page': '10'})
        assert 'Page 10 of 10.' in response.content.decode()
        assert 'next' not in response.content.decode()
        assert 'previous' in response.content.decode()
        