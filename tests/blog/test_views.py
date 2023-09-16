import pytest
from django.urls import reverse
from blog.factory import PostFactory

@pytest.fixture()
def setup_one_item():
    return PostFactory.create(
        title = 'post title',
        sub_title = 'post subtitle',
        content = 'post content',
    )

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
    
    def test_view_pagination_for_one_hundred_post(self, client, setup_one_hundred_items):
        response = client.get(reverse('blog.list'), {'page': '2'})
        assert len(response.context.get('object_list')) == 10

@pytest.mark.django_db
class TestPostDetailView:
    def test_view_returns_200_status_code(self, client, setup_one_item):
        response = client.get(reverse('blog.detail', args=[setup_one_item.slug]))
        assert response.status_code == 200
    
    def test_view_returns_404_status_code_when_post_not_found(self, client):
        response = client.get(reverse('blog.detail', args=['non-exist-post']))
        assert response.status_code == 404
    
    def test_view_render_content_correctly(self, client, setup_one_item):
        response = client.get(reverse('blog.detail', args=[setup_one_item.slug]))
        assert setup_one_item.title in response.rendered_content
        assert setup_one_item.sub_title in response.rendered_content
        assert setup_one_item.content in response.rendered_content