import factory
from faker import Faker
from django.contrib.auth.models import User
from .models import Post, Comment

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('email')
    
    class Meta:
        model = User
        django_get_or_create = ('username',)
        skip_postgeneration_save = True

class CommentFactory(factory.django.DjangoModelFactory):
    email = factory.Faker('email')
    content = factory.Faker('sentence', nb_words=12)
    class Meta:
        model = Comment

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
                self.tags.add(fake.word())
    
    @factory.post_generation
    def comments(self, create, extracted, **kargs):
        if not create:
            return 
        else:
            for i in range(5):
                self.comments.add(CommentFactory(
                    post_id=self.id
                ))