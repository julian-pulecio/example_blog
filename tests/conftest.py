from pytest_factoryboy import register

from blog.factory import UserFactory, PostFactory

register(UserFactory)
register(PostFactory)