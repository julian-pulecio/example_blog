import factory
from django.contrib.auth.models import User
from .models import Post

class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('email')
    
    class Meta:
        model = User
        django_get_or_create = ('username',)
        skip_postgeneration_save = True

class PostFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence', nb_words=12)
    sub_title = factory.Faker('sentence', nb_words=12)
    content = factory.Faker('paragraph', nb_sentences=5)
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Post
        skip_postgeneration_save = True

    @factory.post_generation
    def tags(self, create, extracted, **kargs):
        if not create:
            return 
        else:
            for i in range(5):
                self.tags.add(factory.Faker('name').__str__())