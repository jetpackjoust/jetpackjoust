from datetime import datetime
from django.utils.text import slugify
from django.test import TestCase
from factory.fuzzy import FuzzyNaiveDateTime
import apps.articles.models as models
import taggit.models
import factory
import random
import os


def random_word(n):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    return ''.join([random.choice(letters) for i in range(n)])


class AuthorFactory(factory.django.DjangoModelFactory):
    """Factory for model Author in articles app.
    """
    FACTORY_FOR = models.Author

    last_name = factory.Sequence(lambda n: "Test last name {0}".format(n))
    first_name = factory.Sequence(lambda n: "Test first name {0}".format(n))
    email = factory.LazyAttribute(lambda n: "{0}.{1}@example.com".format(n.first_name,
                                                                         n.last_name))
    contributor_slug = factory.LazyAttribute(lambda n: slugify("{0}-{1}".format(n.first_name,
                                                                                n.last_name)))


class ArticleFactory(factory.django.DjangoModelFactory):
    """Factory for model Article in articles app.
    """
    FACTORY_FOR = models.Article

    title = factory.Sequence(lambda n: "{0}".format(random_word(20)))
    author = factory.SubFactory(AuthorFactory)
    content = factory.Sequence(lambda n: "Test content {0}".format(n))
    summary = factory.Sequence(lambda n: "Test summary {0}".format(n))
    slug = factory.LazyAttribute(lambda n: slugify(n.title))
    published = FuzzyNaiveDateTime(datetime(2012, 1, 1))
    last_modified = factory.LazyAttribute(lambda n: n.published)


class TagFactory(factory.django.DjangoModelFactory):
    """Factory for taggit.models Tag.
    """
    FACTORY_FOR = taggit.models.Tag

    name = factory.Sequence(lambda n: "Test tag {0}".format(n))
    slug = factory.LazyAttribute(lambda n: slugify(n.name))


class CoverImageFactory(factory.django.DjangoModelFactory):
    """Factory for model Cover Image in articles app
    """
    FACTORY_FOR = models.CoverImage
    article = factory.SubFactory(ArticleFactory)
    source = factory.django.ImageField(from_path=os.path.join(os.getcwd(),
                                                              'development',
                                                              'test_images',
                                                              'test_image_1.jpg'))
    caption = factory.Sequence(lambda n: "Test caption {0}".format(n))


class ImageFactory(factory.django.DjangoModelFactory):
    """Factory for model Image in articles app
    """
    FACTORY_FOR = models.Image

    article = factory.SubFactory(ArticleFactory)
    source = factory.django.ImageField(from_path=os.path.join(os.getcwd(),
                                                              'development',
                                                              'test_images',
                                                              'test_image_2.jpg'))
    caption = factory.Sequence(lambda n: "Test caption {0}".format(n))


class TaggedArticleFactory(factory.django.DjangoModelFactory):
    """Factory for through model that links many to many tags to articles.
    """
    FACTORY_FOR = models.TaggedArticle

    tag = factory.SubFactory(TagFactory)
    content_object = factory.SubFactory(ArticleFactory)


class TaggedArticleTwoTagsFactory(ArticleFactory):
    """Factory that returns Article object and creates related tags.
    """
    tag_1 = factory.RelatedFactory(TaggedArticleFactory, 'content_object')
    tag_2 = factory.RelatedFactory(TaggedArticleFactory, 'content_object')


class TaggedArticleThreeTagsFactory(ArticleFactory):
    """Factory that returns Article object and creates related tags.
    """
    tag_1 = factory.RelatedFactory(TaggedArticleFactory, 'content_object')
    tag_2 = factory.RelatedFactory(TaggedArticleFactory, 'content_object')
    tag_3 = factory.RelatedFactory(TaggedArticleFactory, 'content_object')


