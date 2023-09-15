import pytest

@pytest.mark.django_db
class TestPostModel:
    def test_str_return(self, post_factory):
        post = post_factory(title='post_title')
        assert post.__str__() == 'post_title'