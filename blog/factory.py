import factory
from django.contrib.auth.models import User
from .models import Post

class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('email')
    class Meta:
        model = User
        django_get_or_create = ('username',)

class PostFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence', nb_words=12)
    sub_title = factory.Faker('sentence', nb_words=12)
    content = factory.Faker('paragraph', nb_sentences=5)
    slug = factory.Faker('slug')

    class Meta:
        model = Post
    author = factory.SubFactory(UserFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kargs):
        if not create:
            return 
        else:
            for i in range(5):
                self.tags.add(factory.Faker('name').__str__())