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
def setup_pre_set_three_items():
    _ = PostFactory.create(
        title = ' my post title one',
        tags = ['tag1','post','tag3']
    )
    _ = PostFactory.create(
        title = ' my post title two',
        tags = ['tag3','post','tag5']
    )
    _ = PostFactory.create(
        title = 'post title three',
        tags = ['tag6','post','tag8']
    )

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
    
    def test_view_title_filter(self, client, setup_pre_set_three_items):
        response = client.get(reverse('blog.list'), {'title_filter': 'one'})
        assert len(response.context.get('object_list')) == 1

        response = client.get(reverse('blog.list'), {'title_filter': 'my'})
        assert len(response.context.get('object_list')) == 2

        response = client.get(reverse('blog.list'), {'title_filter': 'post'})
        assert len(response.context.get('object_list')) == 3

        response = client.get(reverse('blog.list'), {'title_filter': 'non existing post'})
        assert len(response.context.get('object_list')) == 0
    
    def test_view_tags_filter(self, client, setup_pre_set_three_items):
        
        response = client.get(reverse('blog.list'), {'tags_filter': 'tag1'})    
        assert len(response.context.get('object_list')) == 1
        
        response = client.get(reverse('blog.list'), {'tags_filter': 'tag3'})    
        assert len(response.context.get('object_list')) == 2
        
        response = client.get(reverse('blog.list'), {'tags_filter': 'post'})    
        assert len(response.context.get('object_list')) == 3
        
        response = client.get(reverse('blog.list'), {'tags_filter': 'non existing tag'})    
        assert len(response.context.get('object_list')) == 0

    def test_view_tags_filter_and_title_filter(self, client, setup_pre_set_three_items):
        
        response = client.get(reverse('blog.list'), {'tags_filter': 'tag3', 'title_filter': 'title'})    
        assert len(response.context.get('object_list')) == 2

        response = client.get(reverse('blog.list'), {'tags_filter': 'tag3', 'title_filter': 'one'})    
        assert len(response.context.get('object_list')) == 1

@pytest.mark.django_db
class TestPostDetailView:
    def test_view_returns_200_status_code(self, client, setup_one_item):
        response = client.get(reverse('blog.detail', args=[setup_one_item.slug]))
        assert response.status_code == 200
    
    def test_view_uses_the_correct_template(self, client, setup_one_item):
        response = client.get(reverse('blog.detail', args=[setup_one_item.slug]))
        assert 'post/post_detail.html' in [ template.name for template in response.templates]
    
    def test_view_returns_404_status_code_when_post_not_found(self, client):
        response = client.get(reverse('blog.detail', args=['non-exist-post']))
        assert response.status_code == 404
    
    def test_view_render_content_correctly(self, client, setup_one_item):
        response = client.get(reverse('blog.detail', args=[setup_one_item.slug]))
        assert setup_one_item.title in response.rendered_content
        assert setup_one_item.sub_title in response.rendered_content
        assert setup_one_item.content in response.rendered_content
        assert 'create_comment_form' in response.context_data
        assert 'post_share_form' in response.context_data

    def test_post_detail_view_post_comment(self, client, setup_one_item):
        comments_count = setup_one_item.comments.count()
        response = client.post(
            reverse('blog.detail',args=[setup_one_item.slug]),
            data={'email': 'developer@julianpulecio.com', 'content': 'ASDASDAS', 'comment': ''}
        )
        assert response.status_code == 302
        assert setup_one_item.comments.count() == comments_count + 1

    def test_post_detail_view_share_post(self, client, setup_one_item):
        response = client.post(
            reverse('blog.detail',args=[setup_one_item.slug]),
            data={'email': 'developer@julianpulecio.com', 'share': ''}
        )
        assert response.status_code == 302
    
    def test_post_detail_view_post_comment_form_render_errors(self, client, setup_one_item):
        comments_count = setup_one_item.comments.count()
        response = client.post(
            reverse('blog.detail',args=[setup_one_item.slug]),
            data={'email': 'this is not an email', 'content': 'ASDASDAS', 'comment': ''}
        )
        assert response.status_code == 200
        assert setup_one_item.comments.count() == comments_count
        assert 'Enter a valid email address.' in response.rendered_content
    
    def test_post_detail_view_share_post_form_render_errors(self, client, setup_one_item):
        response = client.post(
            reverse('blog.detail',args=[setup_one_item.slug]),
            data={'email': 'this is not an email', 'share': ''}
        )
        assert response.status_code == 200
        assert 'Enter a valid email address.' in response.rendered_content