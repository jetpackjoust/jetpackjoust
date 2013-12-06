import apps.articles.models as models
import taggit.models
import factory
import random
import os
import unittest
from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.test import TestCase

from factory.fuzzy import FuzzyNaiveDateTime


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
                                                              'test image 1.jpg'))
    caption = factory.Sequence(lambda n: "Test caption {0}".format(n))


class ImageFactory(factory.django.DjangoModelFactory):
    """Factory for model Image in articles app
    """
    FACTORY_FOR = models.Image

    article = factory.SubFactory(ArticleFactory)
    source = factory.django.ImageField(from_path=os.path.join(os.getcwd(),
                                                              'development',
                                                              'test_images',
                                                              'test image 2.jpg'))
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


class TestPadDate(unittest.TestCase):
    """Tests function articles.models.pad_date that adds takes datetime tuples
    and returns tuple of strings with padded zeroes to create pretty dates.
    """
    def setUp(self):
        self.date_1 = (2013, 1, 1)
        self.date_2 = (2013, 11, 11)


    def test_pad_date(self):
        padded_date_1 = models.pad_date(self.date_1)
        padded_date_2 = models.pad_date(self.date_2)
        self.assertEqual(('2013', '01', '01'), padded_date_1)
        self.assertEqual(('2013', '11', '11'), padded_date_2)


class TestSlugifyFile(unittest.TestCase):
    """Tests function articles.models.slugify_file to ensure that the
    string filename gets returned slugified and with extension intact.
    """
    def setUp(self):
        self.none = "manning face"
        self.single = "manning face.png"
        self.multiple = "manning . face. png"

    def test_slugify_file(self):
        slugified_none = models.slugify_file(self.none)
        slugified_single = models.slugify_file(self.single)
        slugified_multiple = models.slugify_file(self.multiple)
        self.assertEqual("manning-face", slugified_none)
        self.assertEqual("manning-face.png", slugified_single)
        self.assertEqual("manning-face.png", slugified_multiple)


class TestArticle(unittest.TestCase):
    """Tests related to model articles.models.Article.
    """
    def setUp(self):
        instance = datetime(2013, 12, 6, 6, 48)
        self.article = TaggedArticleThreeTagsFactory(published=instance)

    def test_get_absolute_url(self):
        url = '/articles/2013/12/06/{0}'.format(self.article.slug)
        self.assertEqual(url, self.article.get_absolute_url())

    def test_get_tags_urls(self):
        template = '/articles/tags/{0}'
        tags = [{'name': tag.name, 'url': template.format(slugify(str(tag)))}
                for tag in self.article.tags.all()]
        self.assertEqual(tags, self.article.get_tags_urls())

    def test_slugify(self):
        self.assertEqual(slugify(self.article.title), self.article.slug)


class TestAuthor(unittest.TestCase):
    """Tests related to model articles.models.Author.
    """
    def setUp(self):
        self.author = AuthorFactory(last_name="Gauss",
                                    first_name="Carl")

    def test_get_absolute_url(self):
        url = '/articles/contributors/carl-gauss'
        self.assertEqual(url, self.author.get_absolute_url())

    def test_slugify(self):
        self.assertEqual("carl-gauss", self.author.contributor_slug)


class TestCoverImage(unittest.TestCase):
    """Tests related to model articles.models.CoverImage.
    """
    def setUp(self):
        self.cover_image = CoverImageFactory()

    def test_get_image_path(self):
        date_string = self.cover_image.article.published.date().strftime('%Y-%m-%d')
        slug = self.cover_image.article.slug
        location = os.path.join('articles', 'images', date_string, slug,
                                'cover_image', 'test-image-1.jpg')
        result = self.cover_image.get_image_path('test image 1.jpg')
        self.assertEqual(location, result)


class TestImage(unittest.TestCase):
    """Tests related to model articles.models.Image.
    """
    def setUp(self):
        self.image = ImageFactory()

    def test_get_image_path(self):
        date_string = self.image.article.published.date().strftime('%Y-%m-%d')
        slug = self.image.article.slug
        location = os.path.join('articles', 'images', date_string, slug,
                                'test-image-2.jpg')
        result = self.image.get_image_path('test image 2.jpg')
        self.assertEqual(location, result)
